def str_answer(answers):
    return "".join([f"Ник пользователя: {answer['username']}\n"
                    f"ID пользователя: {answer['user_id']}\n"
                    f"Ответ: {answer['text']}\n" for answer in answers])


