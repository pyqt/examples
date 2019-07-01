# PyQt Thread example

This example shows how you can use threads to make your PyQt application more responsive. It's a fully functional chat client.

<p align="center"><img src="../screenshots/pyqt-thread-example.png" alt="PyQt Thread Example"></p>

To run this example, please follow [the instructions in the README of this repository](../../README.md#running-the-examples). Instead of `python main.py`, use `python` to execute one of the scripts described below. Eg. `python 01_single_threaded.py`.

To demonstrate the utility of threads, this directory contains multiple implementations of the chat client:

 * [`01_single_threaded.py`](01_single_threaded.py) does not use threads. Once per second, it fetches the latest messages from the server. It does this in the main thread. While fetching messages, it's unable to process your key strokes. As a result, it sometimes lags a little as you type.
 * [`02_multithreaded.py`](02_multithreaded.py) uses threads to fetch new messages in the background. It is considerably more responsive than the single threaded version.
 * [`03_with_threadutil.py`](03_with_threadutil.py) is a variation of the multithreaded version. It extracts the logic necessary for communicating between threads into a separate module that you can use in your own apps, [`threadutil.py`](threadutil.py). For an even more powerful implementation, see [`threadutil_blocking.py`](threadutil_blocking.py). This is the code which [fman](https://fman.io) uses.

Most of the added complexity of the multithreaded versions comes from having to synchronize the main and background threads. In more detail: The _main thread_ is the thread in which Qt draws pixels on the screen, processes events such as mouse clicks, etc. In the examples here, there is a single background thread which fetches messages from the server. But what should happen when a new message arrives? The background thread can't just draw the text on the screen, because Qt might just be in the process of drawing itself. The answer is that the background thread must somehow get Qt to draw the text in the main thread. The second and third examples presented here ([`02_multithreaded.py`](02_multithreaded.py) and [`03_with_threadutil.py`](03_with_threadutil.py)) use different ways of achieving this. In the former, the background thread appends messages to a list, which is then processed in the main thread. The latter uses a custom mechanism that lets the background thread execute arbitrary code in the main thread. In this case, the "arbitrary code" draws the text for the new message on the screen.
