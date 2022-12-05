#include "esphome.h"

using namespace esphome;

Color effect_color(int color_id) {
    light::LightState* c;
    float r, g, b;

    if (color_id % 4 == 0) {
        c = effect_color_1;
    } else if (color_id % 4 == 1) {
        c = effect_color_2;
    } else if (color_id % 4 == 2) {
        c = effect_color_3;
    } else {
        c = effect_color_4;
    }
    c->current_values_as_rgb(&r, &g, &b);
    return Color(r*255, g*255, b*255);
}