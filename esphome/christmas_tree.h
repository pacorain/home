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

void do_solid_color_effect(AddressableLight &it, int num_colors = 4) {
    for (int i = it.size() - 1; i >= 0; i--) {
        it[i] = effect_color(i % num_colors);
    }
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

void do_solid_fade_effect(AddressableLight &it, int num_colors = 4) {
    const uint16_t static_time = 5000;
    const uint16_t transition_time = 3000;

    static uint32_t next_state = millis() + static_time;
    static uint8_t transition_state = false;
    static uint8_t color_state = 0;

    uint32_t now = millis();

    if (!transition_state && now < next_state) {
        it.all() = effect_color(color_state);
    } else if (!transition_state) {
        transition_state = true;
        next_state = now + transition_time;
    }

    if (transition_state && now < next_state) {
        float gradient_amount = (float) (transition_time - (next_state - now)) / transition_time;
        Color new_color = effect_color(color_state).gradient(effect_color((color_state + 1) % num_colors), gradient_amount * 256);
        it.all() = new_color;
    } else if (transition_state) {
        color_state = (color_state + 1) % num_colors;
        transition_state = false;
        next_state = now + static_time;
    }
}

void do_cycle_effect(AddressableLight &it, int num_colors = 4) {
    const uint16_t cycle_time = 8000;

    static uint32_t cycle_start = millis();

    uint16_t num_lights = it.size();
    uint32_t now = millis();
    Color color1, color2;
    uint16_t light_state;
    uint8_t color_step;
    uint16_t step_state;
    float gradient_amount;

    if (now > cycle_start + cycle_time) {
        cycle_start = now;
    }

    uint16_t cycle_offset = now - cycle_start;
    uint16_t step_time = ceil(cycle_time / num_colors);

    for (int i = it.size() - 1; i >= 0; i--) {
        light_state = (cycle_offset + (i * floor(cycle_time / num_lights))) % cycle_time;
        color_step = (uint8_t) (num_colors * light_state / cycle_time);
        color1 = effect_color(color_step);
        color2 = effect_color((color_step + 1) % num_colors);
        
        step_state = light_state % step_time;
        gradient_amount = max(min((float) ((step_state * 2) - (step_time)) / step_time, 1.0f), 0.0f);
        it[i] = color1.gradient(color2, (float) 256 * gradient_amount);
    }
}