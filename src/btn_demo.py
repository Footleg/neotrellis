# Example demo class for an interactive game on the NeoTrellis matrix

# Copyright (C) 2023 Paul 'Footleg' Fretwell

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

OFF = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 80, 0)
YELLOW = (255, 180, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
MAGENTA = (255, 0, 255)
PURPLE = (100, 0, 255)
WHITE = (255,255,255)
DIMWHITE = (20,20,20)

"""
Example class for the NeoTrellis matrix showing how button presses, 
setting and getting button colours and playing sounds can be done.
"""
class BtnDemo:
    def __init__(self, host):
        # Host contains all the RGB LED access and audio play methods of the hardware
        self.host = host
               
    def btnEvent(self, x, y, press):
        if press:
            # Light up button to indicate pressed
            self.host.setColour(x,y,WHITE,False)
            
            # Play sound for this button
            if y == 0:
                if x == 0:
                    self.host.play('swing0')
                elif x == 1:
                    self.host.play('hit')
                elif x == 2:
                    self.host.play('hit0')
                elif x == 3:
                    self.host.play('hit1')
                elif x == 4:
                    self.host.play('hit2')
                elif x == 5:
                    self.host.play('glass_break')
                elif x == 6:
                    self.host.play('glass_break')
                elif x == 7:
                    self.host.play('glass_break')
                elif x == 8:
                    self.host.play('glass_break')
                elif x == 9:
                    self.host.play('glass_break')
                elif x == 10:
                    self.host.play('glass_break')
                elif x == 11:
                    self.host.play('glass_break')
            elif y == 1:
                if x == 0:
                    self.host.play('glass_break')
                elif x == 1:
                    self.host.play('SeaMineExplosion_2')
                elif x == 2:
                    self.host.play('WaterSplash_2')
                elif x == 3:
                    self.host.play('QuickBombDrop_2')
                elif x == 4:
                    self.host.play('EpicExplosion_2')
                elif x == 5:
                    self.host.play('Alert')
                elif x == 6:
                    self.host.play('ArcadeAction01')
                elif x == 7:
                    self.host.play('ArcadeAction04')
                elif x == 8:
                    self.host.play('ArcadeAlarm01')
                elif x == 9:
                    self.host.play('ArcadeAlarm02')
                elif x == 10:
                    self.host.play('ArcadeBeep03')
                elif x == 11:
                    self.host.play('ArcadeChirp03')
            elif y == 2:
                if x == 0:
                    self.host.play('ArcadeChirp07')
                elif x == 1:
                    self.host.play('ArcadeChirp08')
                elif x == 2:
                    self.host.play('ArcadeChirpDescend01')
                elif x == 3:
                    self.host.play('ArcadeChirpDescend02')
                elif x == 4:
                    self.host.play('ArcadeMovement08')
                elif x == 5:
                    self.host.play('ArcadePowerUp01')
                elif x == 6:
                    self.host.play('ArcadePowerUp02')
                elif x == 7:
                    self.host.play('ArcadePowerUp03')
                elif x == 8:
                    self.host.play('BombFall01')
                elif x == 9:
                    self.host.play('CarHorn01')
                elif x == 10:
                    self.host.play('CarHorn02')
                elif x == 11:
                    self.host.play('ChickenCrow')
            elif y == 3:
                if x == 0:
                    self.host.play('ComicalDescent')
                elif x == 1:
                    self.host.play('ComicalMetalGong')
                elif x == 2:
                    self.host.play('ComicalPopwirl')
                elif x == 3:
                    self.host.play('GameOver01')
                elif x == 4:
                    self.host.play('alarm_tone')
                elif x == 5:
                    self.host.play('alert_quick_chime')
                elif x == 6:
                    self.host.play('alien_radio_frequency_call')
                elif x == 7:
                    self.host.play('alien_technology_hum')
                elif x == 8:
                    self.host.play('arcade_bonus_alert')
                elif x == 9:
                    self.host.play('axe_hits_to_plate')
                elif x == 10:
                    self.host.play('bad_joke_drums')
                elif x == 11:
                    self.host.play('bonus_earned_video_game')
            elif y == 4:
                if x == 0:
                    self.host.play('cartoon_alert')
                elif x == 1:
                    self.host.play('cartoon_kitty_begging_meow')
                elif x == 2:
                    self.host.play('chickens_pigeons')
                elif x == 3:
                    self.host.play('confirmation_tone')
                elif x == 4:
                    self.host.play('cow_moo_in_the_barn')
                elif x == 5:
                    self.host.play('donkey_scream')
                elif x == 6:
                    self.host.play('double_beep_tone_alert')
                elif x == 7:
                    self.host.play('electronics_power_up')
                elif x == 8:
                    self.host.play('failure_arcade_alert_notification')
                elif x == 9:
                    self.host.play('fantasy_game_sweep_notification')
                elif x == 10:
                    self.host.play('flute_alert')
                elif x == 11:
                    self.host.play('flute_cell_phone_alert')
            elif y == 5:
                if x == 0:
                    self.host.play('flute_mobile_phone_notification_alert')
                elif x == 1:
                    self.host.play('funny_magic_zoom')
                elif x == 2:
                    self.host.play('futuristic_cinematic_sweep')
                elif x == 3:
                    self.host.play('futuristic_sci_fi_computer_ambience')
                elif x == 4:
                    self.host.play('futuristic_transition_sweep')
                elif x == 5:
                    self.host.play('futuristic_zoom_move')
                elif x == 6:
                    self.host.play('game_notification_wave_alarm')
                elif x == 7:
                    self.host.play('game_success_alert')
                elif x == 8:
                    self.host.play('game_warning_quick_notification')
                elif x == 9:
                    self.host.play('goat_single_baa')
                elif x == 10:
                    self.host.play('happy_bell_alert')
                elif x == 11:
                    self.host.play('high_tech_bleep')
            elif y == 6:
                if x == 0:
                    self.host.play('high_tech_bleep_confirmation')
                elif x == 1:
                    self.host.play('high_tech_notification_bleep')
                elif x == 2:
                    self.host.play('industry_alarm_tone')
                elif x == 3:
                    self.host.play('interface_option_select')
                elif x == 4:
                    self.host.play('magic_notification_ring')
                elif x == 5:
                    self.host.play('mechanical_alert')
                elif x == 6:
                    self.host.play('musical_alert_notification')
                elif x == 7:
                    self.host.play('musical_flute_alert')
                elif x == 8:
                    self.host.play('old_telephone_ring')
                elif x == 9:
                    self.host.play('police_short_whistle')
                elif x == 10:
                    self.host.play('retro_confirmation_tone')
                elif x == 11:
                    self.host.play('rooster_crowing_in_the_morning')
            elif y == 7:
                if x == 0:
                    self.host.play('sci_fi_battle_laser_shots')
                elif x == 1:
                    self.host.play('sci_fi_computer_technology_a')
                elif x == 2:
                    self.host.play('futuristic_sci_fi_computer_ambience_b')
                elif x == 3:
                    self.host.play('sci_fi_error_alert')
                elif x == 4:
                    self.host.play('sci_fi_spaceship_traveling_in_cosmos')
                elif x == 5:
                    self.host.play('shaker_bell_alert')
                elif x == 6:
                    self.host.play('shatter_shot_explosion')
                elif x == 7:
                    self.host.play('shuffling_gear_mech_item')
                elif x == 8:
                    self.host.play('signal_alert')
                elif x == 9:
                    self.host.play('stallion_horse_neigh')
                elif x == 10:
                    self.host.play('technology_notification')
                elif x == 11:
                    self.host.play('unlock_new_item_game_notification')
            elif y == 8:
                if x == 0:
                    self.host.play('QuickBombDrop_1')
                elif x == 1:
                    self.host.play('WaterSplash_1')
                elif x == 2:
                    self.host.play('SeaMineExplosion_1')
                elif x == 3:
                    self.host.play('EpicExplosion_1')
                elif x == 4:
                    self.host.play('uplifting_flute_notification')
                elif x == 5:
                    self.host.play('wolves_pack_howling')
                elif x == 6:
                    self.host.play('Alert')
                elif x == 7:
                    self.host.play('Alert')
                elif x == 8:
                    self.host.play('Alert')
                elif x == 9:
                    self.host.play('sci_fi_computer_technology_b')
                elif x == 10:
                    self.host.play('Alert')
                elif x == 11:
                    self.host.play('Alert')
            elif y == 9:
                if x == 0:
                    self.host.play('QuickBombDrop_2')
                elif x == 1:
                    self.host.play('WaterSplash_2')
                elif x == 2:
                    self.host.play('SeaMineExplosion_2')
                elif x == 3:
                    self.host.play('EpicExplosion_2')
                elif x == 4:
                    self.host.play('sci_fi_computer_technology_a')
                elif x == 5:
                    self.host.play('sci_fi_computer_technology_b')
                elif x == 6:
                    self.host.play('sci_fi_computer_technology_c')
                elif x == 7:
                    self.host.play('sci_fi_computer_technology_e')
                elif x == 8:
                    self.host.play('sci_fi_computer_technology_e')
                elif x == 9:
                    self.host.play('sci_fi_computer_technology_d')
                elif x == 10:
                    self.host.play('sci_fi_computer_technology_e')
                elif x == 11:
                    self.host.play('sci_fi_computer_technology_e')
            elif y == 10:
                if x == 0:
                    self.host.play('QuickBombDrop_3')
                elif x == 1:
                    self.host.play('WaterSplash_3')
                elif x == 2:
                    self.host.play('SeaMineExplosion_3')
                elif x == 3:
                    self.host.play('EpicExplosion_3')
                elif x == 4:
                    self.host.play('sci_fi_computer_technology_a')
                elif x == 5:
                    self.host.play('sci_fi_computer_technology_b')
                elif x == 6:
                    self.host.play('sci_fi_computer_technology_c')
                elif x == 7:
                    self.host.play('sci_fi_computer_technology_e')
                elif x == 8:
                    self.host.play('sci_fi_computer_technology_e')
                elif x == 9:
                    self.host.play('sci_fi_computer_technology_d')
                elif x == 10:
                    self.host.play('sci_fi_computer_technology_e')
                elif x == 11:
                    self.host.play('sci_fi_computer_technology_e')
            elif y == 11:
                if x == 0:
                    self.host.play('QuickBombDrop_4')
                elif x == 1:
                    self.host.play('WaterSplash_4')
                elif x == 2:
                    self.host.play('SeaMineExplosion_4')
                elif x == 3:
                    self.host.play('EpicExplosion_4')
                elif x == 4:
                    self.host.play('sci_fi_computer_technology_a')
                elif x == 5:
                    self.host.play('sci_fi_computer_technology_b')
                elif x == 6:
                    self.host.play('sci_fi_computer_technology_c')
                elif x == 7:
                    self.host.play('sci_fi_computer_technology_e')
                elif x == 8:
                    self.host.play('sci_fi_computer_technology_e')
                elif x == 9:
                    self.host.play('sci_fi_computer_technology_d')
                elif x == 10:
                    self.host.play('sci_fi_computer_technology_e')
                elif x == 11:
                    self.host.play('sci_fi_computer_technology_e')
        else:
            print(f"Colour at {x},{y}: {self.host.getColour(x, y)}")
            if self.host.getColour(x, y) == RED:
                self.host.setColour(x, y, ORANGE)
            elif self.host.getColour(x, y) == ORANGE:
                self.host.setColour(x, y, YELLOW)
            elif self.host.getColour(x, y) == YELLOW:
                self.host.setColour(x, y, GREEN)
            elif self.host.getColour(x, y) == GREEN:
                self.host.setColour(x, y, CYAN)
            elif self.host.getColour(x, y) == CYAN:
                self.host.setColour(x, y, BLUE)
            elif self.host.getColour(x, y) == BLUE:
                self.host.setColour(x, y, MAGENTA)
            elif self.host.getColour(x, y) == MAGENTA:
                self.host.setColour(x, y, PURPLE)
            else:
                self.host.setColour(x, y, RED)

    def animate(self):
        # Increment animations which run independent of button presses (if any)
        None