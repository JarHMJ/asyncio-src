__all__ = 'run',

from . import coroutines
from . import events
from . import tasks


def run(main, *, debug=False):
    """Run a coroutine.
    运行协程。

    This function runs the passed coroutine, taking care of
    managing the asyncio event loop and finalizing asynchronous
    generators.
    此函数运行传入的协程，负责管理 asyncio 事件循环并 完结异步生成器。


    This function cannot be called when another asyncio event loop is
    running in the same thread.
    当有其他 asyncio 事件循环在同一线程中运行时，此函数不能被调用。

    If debug is True, the event loop will be run in debug mode.
    如果 debug 为 True，事件循环将以调试模式运行。

    This function always creates a new event loop and closes it at the end.
    It should be used as a main entry point for asyncio programs, and should
    ideally only be called once.
    此函数总是会创建一个新的事件循环并在结束时关闭之。它应当被用作 asyncio 程序的主入口点，理想情况下应当只被调用一次。

    Example:

        async def main():
            await asyncio.sleep(1)
            print('hello')

        asyncio.run(main())
    """
    if events._get_running_loop() is not None:  # 检查当前是否存在事件循环
        raise RuntimeError(
            "asyncio.run() cannot be called from a running event loop")

    if not coroutines.iscoroutine(main):  # 检查传进来的函数是否为协程对象
        raise ValueError("a coroutine was expected, got {!r}".format(main))

    loop = events.new_event_loop()    # 创建一个事件循环
    try:
        events.set_event_loop(loop)  # 设置为当前的事件循环
        loop.set_debug(debug)
        return loop.run_until_complete(main)
    finally:
        try:
            _cancel_all_tasks(loop)
            loop.run_until_complete(loop.shutdown_asyncgens())
        finally:
            events.set_event_loop(None)
            loop.close()


def _cancel_all_tasks(loop):
    to_cancel = tasks.all_tasks(loop)
    if not to_cancel:
        return

    for task in to_cancel:
        task.cancel()

    loop.run_until_complete(
        tasks.gather(*to_cancel, loop=loop, return_exceptions=True))

    for task in to_cancel:
        if task.cancelled():
            continue
        if task.exception() is not None:
            loop.call_exception_handler({
                'message': 'unhandled exception during asyncio.run() shutdown',
                'exception': task.exception(),
                'task': task,
            })
