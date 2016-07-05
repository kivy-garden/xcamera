# XCamera: Android-optimized camera widget

XCamera is a widget which extends the standard Kivy Camera widget with more
functionality. In particular:

  1. it displays a "shoot button", which the user can press to take pictures

  2. on Android, it uses the native APIs to take high-quality pictures,
     including features such as auto-focus, high resolution, etc.

  3. it includes a method to force landscape mode. On Android, it is often
     desirable to switch to landscape mode when taking pictures: you can
     easily do it by calling "camera.force_landscape()", and later
     "camera.resource_orientation()" to restore the orientation to whatever it
     was before.


![screenshot](/screenshot.jpg?raw=True "Screenshot")
