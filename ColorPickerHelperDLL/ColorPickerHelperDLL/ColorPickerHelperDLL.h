// The following ifdef block is the standard way of creating macros which make exporting 
// from a DLL simpler. All files within this DLL are compiled with the COLORPICKERHELPERDLL_EXPORTS
// symbol defined on the command line. This symbol should not be defined on any project
// that uses this DLL. This way any other project whose source files include this file see 
// COLORPICKERHELPERDLL_API functions as being imported from a DLL, whereas this DLL sees symbols
// defined with this macro as being exported.
#ifdef COLORPICKERHELPERDLL_EXPORTS
#define COLORPICKERHELPERDLL_API __declspec(dllexport)
#else
#define COLORPICKERHELPERDLL_API __declspec(dllimport)
#endif
#include <stdio.h>
#include <Commdlg.h>
#include <WinUser.h>

/* This class is exported from the ColorPickerHelperDLL.dll
class COLORPICKERHELPERDLL_API CColorPickerHelperDLL {
public:
	CColorPickerHelperDLL(void);
	// TODO: add your methods here.
};*/
extern "C" {
	BOOL gotInitDialog = FALSE,
		 gotSetFocus = FALSE,
		 enabled = FALSE,
		 focused = FALSE;
	HWND sublime = NULL;

	UINT_PTR CALLBACK ChooseColorWCallbackHookProc_(HWND hdlg, UINT uiMsg, WPARAM wParam, LPARAM lParam);
	COLORPICKERHELPERDLL_API void __stdcall SetSublimeTextWindow(HWND hWnd);

	COLORPICKERHELPERDLL_API LPCCHOOKPROC ChooseColorWCallbackHookProc = &ChooseColorWCallbackHookProc_;
}
