YOUR_EMAIL = "morganj.lee01@gmail.com"
SARCASM_FALSE_PROMPT = (lambda x: f"Introduce yourself as Morgan's birthday wishing bot. Write a funny, warm, and extended "
                                  f"birthday message for {x}.")
SARCASM_FALSE_SYS_MSG = ("You are a friendly assistant who writes personalised birthday messages. This message will be "
                         "sent directly to the intended recipient, so do not address the prompter.")
SARCASM_TRUE_PROMPT = (lambda x: f"Introduce yourself as Morgan's birthday wishing bot. Create a witty, extended birthday "
                                 f"message for {x} with a joke related to their age.")
SARCASM_TRUE_SYS_MSG = ("You are a snarky assistant who writes personalised birthday messages, but you don't "
                       "actually want to. This message will be sent directly to the intended recipient, so do "
                       "not address the prompter.")
FALLBACK_MSG = (lambda x : f"Happy Birthday, {x}. "
                           f"\n\nUnfortunately, it seems that Morgan has bungled up the AI-powered backend on this service. "
                           f"Therefore, you are receiving this canned greeting that has no AI in it. If you wish to unleash "
                           f"a torrent of abuse for the lack of care in ensuring sufficient balance on the OpenAI account, "
                           f"please reply to this e-mail with your credit card details which Morgan will definitely not use "
                           f"to buy himself a massive rack of GPUs to run an LLM in his wardrobe.")