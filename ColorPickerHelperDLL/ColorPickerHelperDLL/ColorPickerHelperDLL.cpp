#include "stdafx.h"
#include "ColorPickerHelperDLL.h"
extern "C" {

	UINT_PTR CALLBACK ChooseColorWCallbackHookProc_(HWND hdlg, UINT uiMsg, WPARAM wParam, LPARAM lParam)
	{
		// Color Dialog is going to be destroyed/closed,
		// reset everything so the next dialog spawned by the ColorPanel
		// plugin will work properly
		if (uiMsg == WM_DESTROY || uiMsg == WM_CLOSE) {
			gotInitDialog = gotSetFocus = enabled = focused = FALSE;
			sublime = NULL;
		}

		// No associated Sublime Text window, let the dialog process its message
		if (!sublime) {
			return 0;
		}

		if (uiMsg == WM_INITDIALOG && !gotInitDialog) {
			gotInitDialog = TRUE;
		} else if (uiMsg == WM_SETFOCUS && !gotSetFocus) {
			gotSetFocus = TRUE;
		}

		// Re-enable the Sublime Text window
		if (gotInitDialog && !enabled)  {
			BOOL enableResult = EnableWindow(sublime, 1);
			if (enableResult) {
				enabled = TRUE;
			}
		}

		// Give the Sublime Text window focus
		if (gotSetFocus && !focused) {
			HWND setFocusResult = SetFocus(sublime);
			if (setFocusResult) {
				focused = TRUE;
			}
		}
		
		// Don't block any messages
		return 0;
	}

	// Use to let the plugin's run() method indicate what its handle is
	COLORPICKERHELPERDLL_API void __stdcall SetSublimeTextWindow(HWND hWnd) {
		sublime = hWnd;
	}
}