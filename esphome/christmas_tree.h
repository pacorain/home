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

void do_marquee_effect(AddressableLight &it, int num_colors = 4) {
    const uint16_t transition_time = 500;

    static uint16_t offset = 0;
    static uint32_t next_offset = millis() + transition_time;

    if (millis() > next_offset) {
        offset = (offset + 1) % num_colors;
        next_offset = millis() + transition_time;
    }

    for (int i = it.size() - 1; i >= 0; i--) {
        it[i] = effect_color((i + offset) % num_colors);
    }
}