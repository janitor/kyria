# Changing module behavior

If you want to change the behavior of a module that doesn't have any options within vial you will need to change the code in the `users/halcyon_modules/splitkb/<module_name>` folder. Within this folder you can change the `.c`, `.h`, `config.h` or `rules.mk` files to your liking. For the actual configuration options, check out the QMK documentation.

If you want to add any custom `.c` files you can do so by adding a `SRC += <file>.c` to your keymaps `rules.mk` or `SRC += $(CURRENT_DIR)/<file>.c` to the modules `rules.mk`

For the modules we added some extra hooks. Mainly the following:

* `void module_post_init_kb(void)`
* `void module_post_init_user(void)`
* `void module_housekeeping_task_kb(void)`
* `void module_housekeeping_task_user(void)`

These four are added because we already use the `keyboard_post_init_kb` and `housekeeping_task_kb` in the main halcyon code. Any module can then use the other hooks to do anything else.  

* `void display_module_housekeeping_task_kb(bool second_display)`
* `void display_module_housekeeping_task_user(bool second_display)`  

Finally we added a display housekeeping task. We added the feature where the keyboard can detect if there are one or two displays connected. Because we always want to show information about layers if we only have one display, where it doesn't matter where the display is located. We use this to determine if the keyboard with display module is the second display or not and draw the content accordingly.

## Display

To customize your display you will need to add some files to your keymap. A complete example can be found in the `examples` directory in our `qmk_userspace` fork. The files in this example can be added to your keymap folder. Some more simple examples can be found below.

Within the example you can see how a display code should be built up. The functions used here are more thoroughly explained in the [Quantum Painter API documentation from QMK](https://docs.qmk.fm/quantum_painter#quantum-painter-api). Because we added some extra hooks which you can read more about [here](#changing-module-behavior), any actual display initialization is already done so you don't have to worry about that. We make use of the surface feature of quantum painter. This makes it so it only draws changed parts of the display. Which is why we use the `qp_surface_draw` feature at the end of the code. 

There are some quirks when using Quantum Painter which we noticed while creating our firmware which can help if you want to create your own display behavior.
* Font size is determined when generating the file using the CLI.
* You need to generate mono2 fonts if you want to recolor the font but this pretty much breaks any aliased font. So a pixel font is recommended.
* Using pixel fonts you can scale them 2 or 4 times larger but somehow they break at a certain point when going too large. We fixed this by just creating images of the fonts and using that.
* If you want to wrap around text, you'll need to create a custom function for that.
* Drawing a full screen image can give the keyboard noticeable lag. For startup this is okay but switching images every couple of seconds could become annoying.
* This also applies for animations. Smaller size animations are fine, from testing the animations could take up around 30% of the screen and still have the keyboard be responsive but when having animations on the entire screen it can slow down the entire keyboard.
* Using large images or animations can eat up the firmware size very quickly so be aware of that.
* Our displays are 240*135 pixels.

You can also look in the `users/halcyon_modules/hlc_tft_display/` folder to see how we implemented the display code.

To load new fonts or images you will need to convert them using the [Quantum Painter CLI tools.](https://docs.qmk.fm/quantum_painter#quantum-painter-cli)


### Example: draw a picture on the second display

First convert your 240*135 image to a QGF file:
`qmk painter-convert-graphics -f rgb565 -i my_image.png`

Copy the generated files to your keymap.

In your `rules.mk` add

```makefile
SRC += my_image.qgf.c
```

And in your keymap.c add:

```c
#include "hlc_tft_display/hlc_tft_display.h"
#include "qp_surface.h"
#include "my_image.qgf.h"

static painter_image_handle_t my_image;

painter_device_t lcd;
painter_device_t lcd_surface;

bool module_post_init_user(void) {
    return false;
}

bool display_module_housekeeping_task_user(bool second_display) {
    static bool display_set = false;

    if(second_display) {
        if (!display_set) {
            my_image = qp_load_image_mem(gfx_my_image); // Get the `gfx_my_image` from the `my_image.qgf.h` file
            qp_drawimage(lcd_surface, 0, 0, my_image);
        }
    }

    if(!second_display) {
        // Re-use the function to display layers and status
        update_display();
    }

    qp_surface_draw(lcd_surface, lcd, 0, 0, 0);

    return false;
}
```


### Example: write some colorful text on the display

First convert your font to an image file:

```bash
qmk painter-make-font-image -s size_of_font -o ./ -f my_font.ttf
```

Now convert the generated font image

```bash
qmk painter-convert-font-image -f mono2 -i my_font.png
```

In your `rules.mk` add

```makefile
SRC += my_font.qff.c
```

And in your keymap.c add:

```c
#include "hlc_tft_display/hlc_tft_display.h"
#include "qp_surface.h"
#include "my_font.qff.h"

static painter_font_handle_t my_font;

painter_device_t lcd;
painter_device_t lcd_surface;

bool module_post_init_user(void) {
    my_font = qp_load_font_mem(font_my_font);
    static const char *text = "Hello from SplitKB!";
    int16_t width = qp_textwidth(my_font, text);
    qp_drawtext_recolor(lcd_surface, (LCD_WIDTH - width), (LCD_HEIGHT - my_font->line_height), my_font, text, HSV_BLUE, HSV_BLACK);
    qp_surface_draw(lcd_surface, lcd, 0, 0, 0);
    return false;
}

bool display_module_housekeeping_task_user(bool second_display) {
    return false;
}
```

## Encoder

Look at the [QMK documentation for the encoders feature](https://docs.qmk.fm/features/encoders) to see what options are available.

## Cirque

Look at the [QMK documentation for the cirque trackpad](https://docs.qmk.fm/features/pointing_device#cirque-trackpad) to see what options are available.
