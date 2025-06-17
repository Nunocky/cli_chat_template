import signal
import sys
import time
from typing import TYPE_CHECKING, Callable, Generator, Optional

from rich.console import Console
from rich.live import Live
from rich.text import Text

if TYPE_CHECKING:
    from cli_chatbot import CLIChatbot


class CLIChatbot:
    def __init__(self):
        self.console = Console()
        self.running = False
        self.ps1 = "[green]You: [/green]"  # Default prompt
        self.bot_name = "Bot"

        # Callback functions
        self.on_start: Optional[Callable[["CLIChatbot"], None]] = None
        self.on_input: Optional[Callable[["CLIChatbot", str], None]] = None
        self.on_output: Optional[Callable[["CLIChatbot", str], None]] = None
        self.on_exit: Optional[Callable[["CLIChatbot"], None]] = None
        self.on_error: Optional[Callable[["CLIChatbot", Exception], None]] = None

        # Default processor function (echo)
        self.processor: Callable[[str], Generator[str, None, None]] = (
            self._default_processor
        )

        # Setup signal handlers
        self._setup_signal_handlers()

    def _setup_signal_handlers(self):
        def signal_handler(signum, frame):
            self._exit()

        signal.signal(signal.SIGINT, signal_handler)
        if hasattr(signal, "SIGTSTP"):
            signal.signal(signal.SIGTSTP, signal_handler)

    def _default_processor(self, user_input: str) -> Generator[str, None, None]:
        """Default processor that echoes the input with a prefix"""
        response = f"You said: {user_input}"
        for char in response:
            yield char
            time.sleep(0.01)  # Simulate streaming

    def set_prompt(self, prompt: str):
        """Set the input prompt for the chatbot"""
        self.ps1 = prompt

    def set_processor(self, processor: Callable[[str], Generator[str, None, None]]):
        """Set the text processing function"""
        self.processor = processor

    def set_on_start(self, callback: Callable[["CLIChatbot"], None]):
        """Set the on_start callback"""
        self.on_start = callback

    def set_on_input(self, callback: Callable[["CLIChatbot", str], None]):
        """Set the on_input callback"""
        self.on_input = callback

    def set_on_output(self, callback: Callable[["CLIChatbot", str], None]):
        """Set the on_output callback"""
        self.on_output = callback

    def set_on_exit(self, callback: Callable[["CLIChatbot"], None]):
        """Set the on_exit callback"""
        self.on_exit = callback

    def set_on_error(self, callback: Callable[["CLIChatbot", Exception], None]):
        """Set the on_error callback"""
        self.on_error = callback

    def _handle_error(self, error: Exception):
        """Handle errors and call error callback if set"""
        if self.on_error:
            try:
                self.on_error(self, error)
            except Exception as callback_error:
                self.console.print(
                    f"[red]Error in error callback: {callback_error}[/red]"
                )
        else:
            self.console.print(f"[red]Error: {error}[/red]")

    def _exit(self):
        """Handle exit sequence"""
        self.running = False
        if self.on_exit:
            try:
                self.on_exit(self)
            except Exception as e:
                self._handle_error(e)
        sys.exit(0)

    def _stream_output(self, text_generator: Generator[str, None, None]) -> str:
        """Stream output with rich formatting"""
        full_text = ""
        text_obj = Text()

        with Live(text_obj, console=self.console, refresh_per_second=30) as live:
            for chunk in text_generator:
                full_text += chunk
                text_obj.plain = full_text
                live.update(text_obj)

        return full_text

    def print(self, message: str):
        """Print a message to the console with rich formatting"""
        self.console.print(message)

    def run(self):
        """Start the chat interface"""
        self.running = True

        # Call on_start callback
        if self.on_start:
            try:
                self.on_start(self)
            except Exception as e:
                self._handle_error(e)

        # self.console.print(
        #     "[green]CLI Chatbot started. Type '/quit' or press Ctrl-D to exit.[/green]"
        # )

        while self.running:
            try:
                # Get user input
                if sys.stdin.isatty():
                    self.console.print(self.ps1, end="")
                    user_input = input().strip()
                else:
                    # Non-interactive mode
                    user_input = sys.stdin.readline().strip()
                    if not user_input:
                        break

                # Check for quit command
                if user_input.strip() == "/quit":
                    self._exit()
                    break

                # Call on_input callback
                if self.on_input:
                    try:
                        self.on_input(self, user_input)
                    except Exception as e:
                        self._handle_error(e)

                # Process input and stream output
                # self.console.print(self.bot_name + "\n", end="")
                try:
                    output_generator = self.processor(user_input)
                    full_output = self._stream_output(output_generator)

                    # Call on_output callback
                    if self.on_output:
                        try:
                            self.on_output(self, full_output)
                        except Exception as e:
                            self._handle_error(e)

                except Exception as e:
                    self._handle_error(e)

                self.console.print()  # Add newline

            except (EOFError, KeyboardInterrupt):
                # Handle Ctrl-D (Unix) or Ctrl-Z (Windows)
                self._exit()
                break
            except Exception as e:
                self._handle_error(e)
