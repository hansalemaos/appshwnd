import re
from ctypes import LibraryLoader, WinDLL
from ctypes.wintypes import HWND
from time import time
from ctypes_window_info import get_window_infos
from flexible_partial import FlexiblePartialOwnName

windll = LibraryLoader(WinDLL)
user32 = windll.user32


def _restore_window_name(
    hwnd: int | HWND, startwindowtext: str, updatedwindowtext: str
) -> None:
    r"""
       Restore the original window name if it has been changed.
    Args:
        hwnd (int or wintypes.HWND): The handle of the window.
        startwindowtext (str): The original window name.
        updatedwindowtext (str): The updated window name.
    Returns:
        None
    """
    if updatedwindowtext != startwindowtext:
        try:
            hwnd2 = int(hwnd)
            hwndc = HWND(hwnd2)
        except Exception:
            hwndc = hwnd

        user32.SetWindowTextW(hwndc, startwindowtext)


def find_window_and_make_best_window_unique(
    searchdict: dict,
    timeout: float | int = 5,
    make_unique: bool = True,
    *args,
    **kwargs,
):
    r"""
        Search for the window that matches the given criteria dictionary and makes its window title unique (if desired).
    Args:
        searchdict (dict): The dictionary that contains the search criteria for the window.
        timeout (float or int): The time in seconds to wait for making the window unique. Defaults to 5.
        make_unique (bool): Whether to make the window unique or not. Defaults to True.
        *args: Passed to re.search .
        **kwargs: Passed to re.search
    Returns:
        A tuple of best windows, best window, hwnd, start window text, updated window text, and revert name function.
    """
    bestwindows, bestwindow = _find_best_matching_window(searchdict, *args, **kwargs)
    hwnd = bestwindow.hwnd
    startwindowtext = bestwindow.windowtext
    updatedwindowtext = startwindowtext
    timeouttotal = time() + timeout
    if make_unique:
        while timeouttotal > time():
            allwindows = get_window_infos()
            ourwindow = [
                x for x in allwindows if x.hwnd == hwnd and x.status == "visible"
            ]
            windowtext = ourwindow[0].windowtext
            updatedwindowtext = windowtext

            windowswithsametitle = [x for x in allwindows if x.windowtext == windowtext]
            if len(windowswithsametitle) > 1:
                user32.SetWindowTextW(hwnd, windowtext + " ")
            else:
                break
    return (
        bestwindows,
        bestwindow,
        hwnd,
        startwindowtext,
        updatedwindowtext,
        FlexiblePartialOwnName(
            _restore_window_name,
            f"{hwnd} / {repr(startwindowtext)} / {repr(updatedwindowtext)}",
            True,
        ),
    )


def _find_best_matching_window(searchdict: dict, *args, **kwargs):
    r"""
        Find the best matching window for the given criteria dictionary.
    Args:
        searchdict (dict): The dictionary that contains the search criteria for the window.
        *args: Passed to re.search .
        **kwargs: Passed to re.search
    Returns:
        A tuple of best windows and best window.

    """
    allwindows = get_window_infos()

    bestwindows = []
    for w in allwindows:
        bestwindows.append([w])
        for key, item in searchdict.items():
            if not key.endswith("_re"):
                try:
                    if item == (q := getattr(w, key)):
                        bestwindows[-1].append((key, q))
                except Exception:
                    continue
            else:
                try:
                    if re.search(
                        str(item), str(q := getattr(w, key[:-3])), *args, **kwargs
                    ):
                        bestwindows[-1].append((key[:-3], q))
                except Exception:
                    continue

    bestwindows = list(sorted(bestwindows, key=len, reverse=True))
    bestwindow = None
    try:
        bestwindow = bestwindows[0][0]
    except Exception:
        pass
    return bestwindows, bestwindow


def get_invisible_and_visible_windows():
    r"""
        Get information about both visible and invisible windows.
    Args:
        None
    Returns:
        A list of WindowInfo objects for both visible and invisible windows.

    """
    return get_window_infos()


def get_visible_windows():
    r"""
        Get information about visible windows only.
    Args:
        None
    Returns:
        A list of WindowInfo objects for visible windows only.

    """
    return [x for x in get_window_infos() if x.status == "visible"]


def get_invisible_windows():
    r"""
        Get information about invisible windows only.
    Args:
        None
    Returns:
        A list of WindowInfo objects for invisible windows only.

    """
    return [x for x in get_window_infos() if x.status == "invisible"]
