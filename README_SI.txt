මයුරි Telegram AI Bot – සරල Deploy උපදෙස්

වැදගත් ආරක්ෂාව:
- කලින් Telegram Bot Token එක ChatGPT වෙත යවා තිබෙන නිසා BotFather තුළ /revoke කර අලුත් Token එකක් ගන්න.
- Token හෝ Gemini API Key කිසිවෙකුට යවන්න එපා. GitHub code එකට ඒවා ලියන්න එපා.
- Google AI Studio: https://aistudio.google.com/app/apikey
- Render free web service එක විනාඩි 15ක් request නැතිනම් sleep වෙනවා. නැවත request එකක් ආවම අවදි වීමට මිනිත්තුවක් පමණ ගත විය හැක. ඒ නිසා මෙය සහතික 24/7 hosting එකක් නොවේ. Free plan සීමා වෙනස් විය හැක.

1) ZIP එක unzip කරන්න.
2) GitHub account එකක් සාදා New repository එකක් සාදන්න.
3) මේ ZIP එකේ app.py, requirements.txt, render.yaml සහ README_SI.txt files upload කරන්න.
4) https://render.com වෙත ගොස් GitHub එක connect කරන්න.
5) New > Blueprint තෝරා ඔබේ repository එක තෝරන්න.
6) Render විසින් BOT_TOKEN, GEMINI_API_KEY සහ WEBHOOK_SECRET environment variables ඉල්ලයි.
   - BOT_TOKEN: BotFather වෙතින් අලුතින් ගත් Token එක
   - GEMINI_API_KEY: Google AI Studio API key එක
   - WEBHOOK_SECRET: අකුරු/ඉලක්කම් දිගු රහස් අගයක් ඔබම සාදා දාන්න (උදා: Mayuri-... වගේ අනුමාන කළ නොහැකි අගයක්)
7) Deploy අවසන් වූ පසු Render හි service URL එක copy කරන්න. උදා: https://your-service.onrender.com
8) Browser එකේ පහත URL එක සකසා open කරන්න:
   https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=https://your-service.onrender.com/telegram/<YOUR_WEBHOOK_SECRET>
   <YOUR_BOT_TOKEN>, service URL සහ <YOUR_WEBHOOK_SECRET> ඔබේ අගයන්ගෙන් මාරු කරන්න.
9) Telegram හි @Mayuri_Love_AI_Bot open කර /start යවන්න.

Commands:
- /start – කතාබහ පටන් ගන්න
- /reset – එම chat එකේ කෙටි කාලීන මතකය reset කරන්න

සටහන්:
- මෙහි memory එක සරල RAM memory එකක්. Render restart/sleep/redeploy වූ විට මතකය නැතිවෙයි.
- මේ starter version එක text chat සඳහාය; voice messages තවම ඇතුළත් කර නැත.
- Gemini API usage limits/charges ඔබේ Google AI Studio account එකේ තත්ත්වය අනුව වෙනස් විය හැක.
- Render free service එක sleep වන නිසා පළමු පිළිතුර ප්‍රමාද විය හැක.
