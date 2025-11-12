from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from ai_agents import chatgpt_agent, gemini_agent

router = Router()

@router.message(CommandStart())
async def start_handler(message: types.Message, state: FSMContext):
    kb = InlineKeyboardBuilder()
    kb.button(text="🤖 ChatGPT", callback_data="ai_chatgpt")
    kb.button(text="🔮 Gemini", callback_data="ai_gemini")
    kb.adjust(2)
    await message.answer(
        "Вітаю! Обери ШІ для спілкування 👇",
        reply_markup=kb.as_markup()
    )
    await state.clear()

@router.callback_query(lambda c: c.data.startswith("ai_"))
async def select_agent(query: types.CallbackQuery, state: FSMContext):
    agent = query.data.split("_")[1]
    await state.update_data(agent=agent)
    await query.message.edit_text(f"✅ Обрано: {agent.upper()}.\nВведи свій запит:")
    await query.answer()

@router.message()
async def chat_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    agent = data.get("agent")
    if not agent:
        await message.answer("⚠️ Спочатку обери ШІ через /start")
        return

    prompt = message.text
    await message.answer("⏳ Думаю...")

    if agent == "chatgpt":
        answer = await chatgpt_agent.ask(prompt)
    elif agent == "gemini":
        answer = await gemini_agent.ask(prompt)
    else:
        answer = "Невідомий агент 🤔"

    await message.answer(answer)
