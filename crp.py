import gradio as gr
import requests
import json

# Crypto data and responses
CRYPTO_IDS = {
    'bitcoin': 'bitcoin', 'btc': 'bitcoin',
    'ethereum': 'ethereum', 'eth': 'ethereum', 
    'cardano': 'cardanoo', 'ada': 'cardano',
    'solana': 'solana', 'sol': 'solana',
    'dogecoin': 'dogecoin', 'doge': 'dogecoin',
    'litecoin': 'litecoin', 'ltc': 'litecoin',
    'chainlink': 'chainlink', 'link': 'chainlink',
    'polygon': 'matic-network', 'matic': 'matic-network'
}

# Simple responses for common questions
RESPONSES = {
    'hello': "Hey! I'm your crypto bot. Ask me about cryptocurrency prices!",
    'hi': "Hello! Ready to check some crypto prices?",
    'help': "I can help you check cryptocurrency prices. Try asking: 'What's the price of Bitcoin?' or 'How much is ETH?'",
    'thanks': "You're welcome! Ask me about more crypto prices anytime!",
    'bye': "See you later! Keep hodling! 🚀"
}

def get_crypto_price(coin_name):
    """Get cryptocurrency price from CoinGecko API"""
    coin_id = CRYPTO_IDS.get(coin_name.lower(), coin_name.lower())
    
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd&include_24hr_change=true"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if coin_id in data:
                price = data[coin_id]['usd']
                change_24h = data[coin_id].get('usd_24h_change', 0)
                
                emoji = "📈" if change_24h > 0 else "📉" if change_24h < 0 else "➡️"
                change_text = f"({change_24h:+.2f}% 24h)" if change_24h != 0 else ""
                
                return f"💰 {coin_name.upper()}: ${price:,.2f} {emoji} {change_text}"
            else:
                return f"❌ Sorry, couldn't find price for '{coin_name}'. Try: bitcoin, ethereum, solana, cardano, dogecoin"
        else:
            return "⚠️ API request failed. Please try again in a moment."
            
    except Exception as e:
        return f"❌ Error fetching price: Network issue. Please check your connection."

def extract_crypto_mentions(text):
    """Extract cryptocurrency mentions from user input"""
    words = text.lower().split()
    for word in words:
        if word in CRYPTO_IDS:
            return word
    return None

def chatbot_response(user_input):
    """Main chatbot logic"""
    if not user_input or not user_input.strip():
        return "Please enter a message!"
    
    user_input = user_input.strip().lower()
    
    # Check for simple greetings/responses
    for key, response in RESPONSES.items():
        if key in user_input:
            return response
    
    # Check for price requests
    price_keywords = ['price', 'cost', 'worth', 'value', 'much', 'trading']
    if any(keyword in user_input for keyword in price_keywords):
        crypto_coin = extract_crypto_mentions(user_input)
        if crypto_coin:
            return get_crypto_price(crypto_coin)
        else:
            # Try to extract coin name from common patterns
            for coin_name in CRYPTO_IDS.keys():
                if coin_name in user_input:
                    return get_crypto_price(coin_name)
            return "Which cryptocurrency price would you like to check? (e.g., Bitcoin, Ethereum, Solana)"
    
    # Check if crypto is mentioned without explicit price request
    crypto_mentioned = extract_crypto_mentions(user_input)
    if crypto_mentioned:
        return get_crypto_price(crypto_mentioned)
    
    # Default responses for unrecognized input
    if len(user_input) < 3:
        return "Could you be more specific? Ask me about crypto prices!"
    
    return "I specialize in cryptocurrency prices! Try asking: 'What's Bitcoin's price?' or 'How much is Ethereum worth?'"

# Create the Gradio interface
demo = gr.Interface(
    fn=chatbot_response,
    inputs=gr.Textbox(
        placeholder="Ask about crypto prices... (e.g., 'Bitcoin price' or 'How much is ETH?')",
        lines=2
    ),
    outputs=gr.Textbox(lines=3),
    title="🚀 Maina Crypto Bot",
    description="Get real-time cryptocurrency prices! Supports Bitcoin, Ethereum, Solana, Cardano, Dogecoin, and more.",
    examples=[
        "What's Bitcoin's price?",
        "How much is Ethereum worth?", 
        "Solana price",
        "Show me Dogecoin value",
        "What's the cost of Cardano?",
        "Hello!"
    ],
    theme=gr.themes.Soft()
)

if __name__ == "__main__":
    demo.launch(share=True)