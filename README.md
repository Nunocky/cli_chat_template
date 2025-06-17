# CLI Chat Template

[English](README.md) | [日本語](README_ja.md)

Python CLI template for building chat applications.

## Functionality

- It outputs the text entered by the user and the text processed by the computer in response to that input.
- The interaction proceeds as follows:
  - First, the user enters text.
  - The computer processes the text and outputs the result. The processing logic can be defined by the implementer using callback functions, as it varies by application. Output also supports streaming.
  - This cycle repeats until the user exits. Exiting can be done with Ctrl-D (Unix), Ctrl-Z (Windows), or by entering `/quit`.
- The following hooks are also available:
  - on_start: Callback invoked when the application starts
  - on_input: Callback invoked when the user enters text
  - on_output: Callback invoked when the computer outputs text
  - on_exit: Callback invoked when the application exits
  - on_error: Callback invoked when an error occurs
