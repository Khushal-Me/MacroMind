import discord
from discord.ext import commands
import requests
from datetime import datetime, timedelta
import json
import os
from dotenv import load_dotenv
from flask import Flask, jsonify
from threading import Thread

app = Flask(__name__)

# Add a home route for monitoring the bot
@app.route('/')
def home():
    return "Bot is running!"

# Add a status route for monitoring additional details
@app.route('/status')
def status():
    return jsonify({"status": "alive", "uptime": "100%"})

# Define the server function
def run():
    # Run the Flask app on port 8080 with error handling
    try:
        app.run(host='0.0.0.0', port=8080, debug=False)
    except Exception as e:
        print(f"Flask server failed to start: {e}")

# Define the keep_alive function with threading
def keep_alive():
    t = Thread(target=run)
    t.daemon = True  # Ensures the thread exits when the main program does
    t.start()

keep_alive()

load_dotenv()

# Set up intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


# Hardcoded daily limits
DAILY_CALORIES = 2250
DAILY_PROTEIN = 180

# Data to keep track of
user_data = {}

# Your bot token and Gemini API key
BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Gemini API configuration
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

def get_nutritional_info(food_description):
    """
    Get nutritional information using the Gemini API
    """
    headers = {
        "Content-Type": "application/json"
    }
    
    # Craft a specific prompt for the Gemini API
    prompt = f"""
    Please analyze this food item and provide its nutritional information:
    Food: {food_description}
    
    Provide the response in this exact JSON format:
    {{
        "calories": number,
        "protein": number in grams
    }}
    Only provide the JSON, no other text.
    """
    
    payload = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }]
    }
    
    try:
        response = requests.post(
            f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
            headers=headers,
            json=payload
        )
        
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Parse the Gemini response
        result = response.json()
        if 'candidates' in result and len(result['candidates']) > 0:
            text_response = result['candidates'][0]['content']['parts'][0]['text']
            # Extract the JSON from the response
            nutrition_data = json.loads(text_response)
            return nutrition_data
        else:
            raise ValueError("No valid response from Gemini API")
            
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        print(f"Raw response: {text_response}")
        raise
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        raise

def reset_data(user_id):
    user_data[user_id] = {
        'calories': 0,
        'protein': 0,
        'history': [],
        'last_reset': datetime.now()
    }

def ask_gemini(question):
    """
    Get an answer from Gemini API for nutrition-related questions
    """
    headers = {
        "Content-Type": "application/json"
    }
    
    prompt = f"""
    You are a nutrition expert assistant. Answer this nutrition question concisely:
    {question}

    CRITICAL: Your response MUST be under 800 characters while remaining complete and coherent.
    Prioritize the most important information and use concise language.
    If you cannot provide a complete answer within 800 characters, reshape your response to cover 
    the most essential points that will help the user.
    
    For non-nutrition based questions, simply respond: "I can only answer questions about nutrition, food, diet, and health."
    """
    
    payload = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }],
        "generationConfig": {
            "temperature": 0.3,  # Lower temperature for more focused responses
            "maxOutputTokens": 250  # Approximate token limit for 800 chars
        }
    }
    
    try:
        response = requests.post(
            f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
            headers=headers,
            json=payload
        )
        
        response.raise_for_status()
        
        result = response.json()
        if 'candidates' in result and len(result['candidates']) > 0:
            answer = result['candidates'][0]['content']['parts'][0]['text']
            return answer.strip()
        else:
            raise ValueError("No valid response from Gemini API")
            
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        raise


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

@bot.command()
async def add(ctx, *, food_description):
    user_id = ctx.author.id
    
    # Reset the user's data if it's a new day
    if user_id not in user_data or datetime.now() - user_data[user_id]['last_reset'] >= timedelta(days=1):
        reset_data(user_id)

    try:
        # Split by commas, assuming each item is separated by them
        items = [item.strip() for item in food_description.split(",")]
        itemized_entries = []
        total_calories = 0
        total_protein = 0

        # Process each item and format it nicely
        for item in items:
            # Get nutritional information (dummy function here)
            nutrition_info = get_nutritional_info(item)  # Replace with actual function
            
            # Format each item with bolded nutritional values
            item_entry = f"{item} (**Calories:** {nutrition_info['calories']} kcal, **Protein:** {nutrition_info['protein']}g)"
            itemized_entries.append(item_entry)
            
            # Accumulate totals
            total_calories += nutrition_info['calories']
            total_protein += nutrition_info['protein']
        
        # Update user data
        user_data[user_id]['calories'] += total_calories
        user_data[user_id]['protein'] += total_protein
        user_data[user_id]['history'].extend(itemized_entries)

        # Send response with each item on a new line
        response = "Added:\n" + "\n".join(itemized_entries) + f"\n\nDaily totals - **Calories:** {user_data[user_id]['calories']} kcal, **Protein:** {user_data[user_id]['protein']}g"
        await ctx.send(response)

    except Exception as e:
        await ctx.send("Sorry, I couldn't process that food item. Please try again with a more specific description.")
        print(f"Error: {str(e)}")




@bot.command()
async def left(ctx):
    user_id = ctx.author.id

    # Ensure user data exists
    if user_id not in user_data:
        reset_data(user_id)

    calories_left = DAILY_CALORIES - user_data[user_id]['calories']
    protein_left = DAILY_PROTEIN - user_data[user_id]['protein']
    
    await ctx.send(f"You have {calories_left} calories and {protein_left}g of protein left for today.")

@bot.command()
async def history(ctx):
    user_id = ctx.author.id
    
    if user_id not in user_data or not user_data[user_id]['history']:
        await ctx.send("No food history found for today.")
        return
    
    # Format each history entry on a new line
    history_entries = "\n".join(user_data[user_id]['history'])
    
    # Display the formatted history
    response = f"**Food history:**\n{history_entries}"
    await ctx.send(response)


@bot.command()
async def clear(ctx, option=None):
    user_id = ctx.author.id
    
    if user_id not in user_data:
        reset_data(user_id)
    
    if option == 'r':
        # Clear the most recent entry
        if user_data[user_id]['history']:
            last_entry = user_data[user_id]['history'].pop()
            # Extract calories and protein from the last entry
            entry_parts = last_entry.split(' (Calories: ')
            calories_part = entry_parts[1].split(', Protein: ')[0] if len(entry_parts) > 1 else '0'
            protein_part = entry_parts[1].split(', Protein: ')[1][:-1] if len(entry_parts) > 1 else '0'
            
            user_data[user_id]['calories'] -= int(calories_part)
            user_data[user_id]['protein'] -= int(protein_part)

            await ctx.send(f"Cleared most recent entry: {last_entry}")
        else:
            await ctx.send("No entries to clear.")
    else:
        # Clear all entries
        reset_data(user_id)
        await ctx.send("Cleared all data.")

@bot.command()
async def q(ctx, *, question):
    """
    Ask a nutrition-related question and get an answer from Gemini
    Usage: !q What are good sources of protein?
    """
    try:
        # Check if question is too long before making the API call
        if len(question) > 1024:
            await ctx.send("Sorry, your question is too long. Please try to ask a shorter question (under 1024 characters).")
            return
            
        async with ctx.typing():
            answer = ask_gemini(question)
            
            # If answer is too long, make another attempt with a stronger length constraint
            if len(answer) > 1024:
                # Modify the question to emphasize brevity
                abbreviated_question = "Please answer this very briefly: " + question
                answer = ask_gemini(abbreviated_question)
                
                # If still too long, apologize and ask for a more specific question
                if len(answer) > 1024:
                    await ctx.send("I apologize, but I'm having trouble providing a concise answer. Could you try asking a more specific question?")
                    return
            
            embed = discord.Embed(
                title=" ",
                color=discord.Color.green()
            )
            embed.add_field(name="", value=answer, inline=False)
            embed.set_footer(text="Powered by MacroMind")
            
            await ctx.send(embed=embed)
            
    except Exception as e:
        error_message = "Sorry, I couldn't process your question. Please try again."
        if isinstance(e, requests.exceptions.RequestException):
            error_message = "Sorry, I'm having trouble connecting to the nutrition database. Please try again later."
        await ctx.send(error_message)
        print(f"Error in q command: {str(e)}")

# Initialize user data
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)


if __name__ == "__main__":
    # Make sure we got our environment variables
    if not BOT_TOKEN or not GEMINI_API_KEY:
        print("Error: Could not find tokens in .env file!")
        exit(1)
        
    bot.run(BOT_TOKEN)
