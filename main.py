import time

from cli_chatbot import CLIChatbot


def custom_processor(user_input: str):
    """カスタム処理関数の例 - 入力を大文字に変換してゆっくり出力"""
    response = f"処理結果: {user_input.upper()}"
    for char in response:
        yield char
        time.sleep(0.02)


def on_start_callback():
    print("🤖 チャットボットが開始されました！")


def on_input_callback(user_input: str):
    print(f"📝 入力を受信: {len(user_input)}文字")


def on_output_callback(output: str):
    print(f"📤 出力完了: {len(output)}文字")


def on_exit_callback():
    print("👋 チャットボットを終了します")


def on_error_callback(error: Exception):
    print(f"❌ エラーが発生しました: {error}")


def main():
    # チャットボットインスタンスを作成
    chatbot = CLIChatbot()

    # chatbot.set_prompt("> ")
    # コールバック関数を設定
    chatbot.set_on_start(on_start_callback)
    chatbot.set_on_input(on_input_callback)
    chatbot.set_on_output(on_output_callback)
    chatbot.set_on_exit(on_exit_callback)
    chatbot.set_on_error(on_error_callback)

    # カスタム処理関数を設定
    chatbot.set_processor(custom_processor)

    # チャットボットを開始
    chatbot.run()


if __name__ == "__main__":
    main()
