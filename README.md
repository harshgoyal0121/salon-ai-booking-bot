# AI Booking Assistant — Portfolio Demo

An AI-powered booking & FAQ assistant built for a fictional business ("Glow Salon")
to demonstrate how small businesses can automate customer inquiries and bookings
using AI + a simple chat interface (here, Telegram — the same approach adapts to
WhatsApp Business API, Instagram DMs, or a website widget).

## What it does
- Answers customer questions about hours, services, and pricing — grounded only
  in real business facts, so it never invents information
- Collects booking details (name, service, date/time, phone) conversationally
- Logs conversations so a business owner can follow up
- Built to be adapted in under a day for any service business (salons, clinics,
  gyms, coaching centers, repair shops, etc.)

## Tech stack
- Python
- `python-telegram-bot` for the chat interface
- Groq API (Llama 3.3) for the AI responses — free tier, no billing required
- Easily portable to WhatsApp Business API or a website chat widget — the AI
  logic and business-context layer stay the same, only the messaging channel changes

## Setup
1. Message [@BotFather](https://t.me/BotFather) on Telegram, run `/newbot`, and copy your bot token
2. Get a free API key from [console.groq.com](https://console.groq.com) (sign up, go to API Keys, create one — no credit card needed)
3. Copy `.env.example` to `.env` and fill in both keys (or export them directly)
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Run it:
   ```
   python bot.py
   ```
6. Open Telegram, find your bot, and send `/start`

## How to customize this for a real client
Everything a business would need changed lives in one place: the `BUSINESS_CONTEXT`
string in `bot.py`. Swap in the client's actual hours, services, prices, and
policies, and the bot immediately "knows" their business — no other code changes
needed for a basic deployment.

---

## Portfolio case study (use this write-up on Upwork/Contra/LinkedIn)

**Project: AI Booking Assistant for Service Businesses**

*The problem:* Small service businesses (salons, clinics, gyms) lose leads when
they can't answer customer questions instantly — especially outside business
hours or during busy periods when phone calls go unanswered.

*What I built:* An AI-powered chat assistant that answers FAQs (hours, pricing,
services) and collects booking requests conversationally, then logs them for
the business owner to confirm. Built on Telegram for this demo; the same
architecture deploys to WhatsApp Business API or a website widget for a live client.

*How it works:* The assistant is grounded in the business's real information
via a structured context layer, so it never invents facts or hours. It handles
natural conversation (not rigid menu buttons), remembers context within a
session, and hands off gracefully when it doesn't know something.

*Tools used:* Python, python-telegram-bot, Groq API (Llama 3.3)

*Turnaround:* This kind of bot can typically be customized and deployed for a
new business in 1–3 days, depending on complexity (number of services, booking
rules, integrations needed).


Below is the video showing a real conversation with the bot:   
https://github.com/user-attachments/assets/38b37f09-61fd-4cc0-a4ca-193a31434b2f

