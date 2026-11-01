import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# लॉगिंग सेट अप
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# तेरा टेलीग्राम बॉट टोकन
TOKEN = '9074951886:AAHpDpr-8iGLnsUZIdl95g_GWW019twbOuI'

async def handle_prediction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    
    # सभी तरह के सेपरेटर्स (कॉमा, डॉट, डैश, स्लैश) को स्पेस में बदल दें
    for char in [',', '.', '-', '_', '/']:
        text = text.replace(char, ' ')
        
    parts = text.split()
    
    if not parts:
        await update.message.reply_text("कृपया पीरियड नंबर और पिछले नतीजे भेजें!")
        return
        
    # पहला हिस्सा हमेशा पीरियड नंबर होगा
    period_no = parts[0]
    
    # बाकी बचे हिस्सों में से B और S को ढूंढ कर निकालेंगे (चाहे छोटे हों या बड़े)
    history = []
    for item in parts[1:]:
        for char in item.upper():
            if char in ['B', 'S']:
                history.append(char)
                
    # अगर यूजर ने नतीजे नहीं लिखे हैं
    if not history:
        await update.message.reply_text(
            f"🎯 **Period:** {period_no}\n"
            "⚠️ भाई, पीरियड नंबर के साथ पिछले नतीजे (b या s) भी लिखो!"
        )
        return

    # पिछले नतीजों की गिनती करें
    big_count = history.count('B')
    small_count = history.count('S')
    
    # प्रेडिक्शन लॉजिक
    if big_count > small_count:
        pred_letter = "B"
        pred_full = "Big"
    elif small_count > big_count:
        pred_letter = "S"
        pred_full = "Small"
    else:
        pred_letter = "B / S"
        pred_full = "Mix Trend"
        
    # बॉट का शानदार और साफ़ रिप्लाई
    await update.message.reply_text(
        f"🎯 **Period:** {period_no}\n"
        f"📊 **Trend:** {', '.join(history)}\n"
        f"🔮 **Prediction:** **{pred_letter}** ({pred_full})"
    )

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    # टेक्स्ट मैसेज हैंडलर
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_prediction))
    
    print("पीरियड प्रेडिक्शन बॉट शुरू हो गया है...")
    application.run_polling()
    