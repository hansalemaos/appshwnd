# appshwnd

This module provides utilities for finding and manipulating windows in Windows OS. It includes functions for finding windows based on various attributes,  getting information about visible and invisible windows, and making window names unique (e.g. With FFmpeg, you can record a window, but you have to pass the title of the Window which causes problems if there are duplicates. )

## pip install appshwnd


#### ### Tested against Windows 10 / Python 3.10 / Anaconda


### Functions
```python
FUNCTIONS
    find_window_and_make_best_window_unique(searchdict: dict, timeout: float | int = 5, make_unique: bool = True, *args, **kwargs)
            Search for the window that matches the given criteria dictionary and makes its window title unique (if desired).
        Args:
            searchdict (dict): The dictionary that contains the search criteria for the window.
            timeout (float or int): The time in seconds to wait for making the window unique. Defaults to 5.
            make_unique (bool): Whether to make the window unique or not. Defaults to True.
            *args: Passed to re.search .
            **kwargs: Passed to re.search
        Returns:
            A tuple of best windows, best window, hwnd, start window text, updated window text, and revert name function.
    
    get_invisible_and_visible_windows()
            Get information about both visible and invisible windows.
        Args:
            None
        Returns:
            A list of WindowInfo objects for both visible and invisible windows.
    
    get_invisible_windows()
            Get information about invisible windows only.
        Args:
            None
        Returns:
            A list of WindowInfo objects for invisible windows only.
    
    get_visible_windows()
            Get information about visible windows only.
        Args:
            None
        Returns:
            A list of WindowInfo objects for visible windows only.
    
    time(...)
        time() -> floating point number
        
        Return the current time in seconds since the Epoch.
        Fractions of a second may be present if the system clock provides them.



# A dictionary that contains all possible search criteria for finding a window. 
# You can pass as many attributes as you want. The window with the most matches wins. 
searchdict = {
    "pid": 1004,
    "pid_re": "^1.*",
    "title": "IME",
    "title_re": "IM?E",
    "windowtext": "Default IME",
    "windowtext_re": r"Default\s*IME",
    "hwnd": 197666,
    "hwnd_re": r"\d+",
    "length": 12,
    "length_re": "[0-9]+",
    "tid": 6636,
    "tid_re": r"6\d+36",
    "status": "invisible",
    "status_re": "(?:in)?visible",
    "coords_client": (0, 0, 0, 0),
    "coords_client_re": r"\([\d,\s]+\)",
    "dim_client": (0, 0),
    "dim_client_re": "(1?0, 0)",
    "coords_win": (0, 0, 0, 0),
    "coords_win_re": r"\)$",
    "dim_win": (0, 0),
    "dim_win_re": "(1?0, 0)",
    "class_name": "IME",
    "class_name_re": "I?ME$",
    "path": "C:\\Windows\\ImmersiveControlPanel\\SystemSettings.exe",
    "path_re": "SystemSettings.exe",
}

from appshwnd import ( find_window_and_make_best_window_unique,
 get_invisible_and_visible_windows,
 get_invisible_windows,
 get_visible_windows,
 get_window_infos,)
 
 
# Find the window without changing the window title 
(
    bestwindows,  # most matches = first place
    bestwindow,  # WindowInfo object
    hwnd,  # 132762
    startwindowtext,  # 'Default IME'
    updatedwindowtext,  # 'Default IME' (no difference, because of make_unique=False)
    revertnamefunction,  # restore the original name
) = find_window_and_make_best_window_unique(
    searchdict, timeout=5, make_unique=False, flags=re.I
)

# Example search for Notepad 


get_visible_windows()
....
WindowInfo(pid=8896, title='Notepad', windowtext='*Untitled - Notepad', hwnd=2034552, length=20, tid=2772, status='visible', coords_client=(0, 877, 0, 675), dim_client=(877, 675), coords_win=(745, 1638, 324, 1058), dim_win=(893, 734), class_name='Notepad', path='C:\\Windows\\System32\\notepad.exe'),
....
WindowInfo(pid=16852, title='Notepad', windowtext='*Untitled - Notepad', hwnd=657206, length=20, tid=16876, status='visible', coords_client=(0, 877, 0, 675), dim_client=(877, 675), coords_win=(475, 1368, 219, 953), dim_win=(893, 734), class_name='Notepad', path='C:\\Windows\\System32\\notepad.exe')]
....


searchdict = {
    "title": "Notepad",
    "windowtext_re": r"\*+",
    'path_re': '.*notepad.exe.*'
}

# Find the window and make it unique
(
    bestwindows,  # most matches = first place
    bestwindow,  # WindowInfo object
    hwnd,  # window handle
    startwindowtext,  # current window text
    updatedwindowtext,  # updated window text
    revertnamefunction,  # function to restore the original window text
) = find_window_and_make_best_window_unique(
    searchdict, timeout=5, make_unique=True, flags=re.I
)

# Example of restoring the original window text
startwindowtext  # '*Untitled - Notepad'
updatedwindowtext  # '*Untitled - Notepad ' (notice the space at the end - this window title is now unique)
revertnamefunction()  # Restore the old name
startwindowtext  # '*Untitled - Notepad'
updatedwindowtext  # '*Untitled - Notepad'

An example with FFmpeg (to make sure that you are recording the right window)
1) Make the window title unique 
2) Start FFmpeg in a subprocess (Popen)
3) After 2 seconds, you can change the name back: revertnamefunction()

```