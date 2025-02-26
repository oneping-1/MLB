"""
Module that prints a list of pitches' location using matplotlib library.
The plotter method takes in a list of src.Game.PlayEvents. The
PlayEvents class represents pitches in a game.

Classes:
    Plotter: Framework to plot pitches. Plotter.plot() is the most
        important method

Example:
from src.plotter import Plotter
plotter = Plotter()
plotter.plot([GameEvents])
"""

from typing import List
from matplotlib import pyplot as plt
from matplotlib import patches
from at_bat.umpire import MissedCalls

class Plotter:
    """
    Plots missed pitches in a game similar to the box provided by Ump
    Scorecards.

    Class Attributes:
        PLATE_WIDTH_INCH (int): Plate width in inches
        BALL_RADIUS_INCH (int): Ball width in inches

    Instance Attributes:
        sZ_top (float): The top of the strike zone. If only one pitch
            is provided in plot method, the top will change to the top
            of the strike zone for that specific pitch. Defaults to 3.5
        sZ_bot (float): The bottom of the strike zone. If only one pitch
            is provided in plot method, the top will change to the
            bottom of the strike zone for that specific pitch. Defaults
            to 1.5
    """
    PLATE_WIDTH_INCH: float = 17
    _PLATE_WIDTH_FEET: float = PLATE_WIDTH_INCH / 12
    sX_min: float = -_PLATE_WIDTH_FEET / 2
    sX_max: float = _PLATE_WIDTH_FEET / 2
    BALL_RADIUS_INCH: float = 1.437
    _BALL_RADIUS_FEET: float = BALL_RADIUS_INCH / 12

    def __init__(self):
        # default top and bottom strike zone
        self.sz_top: float = 3.5
        self.sz_bot: float = 1.5
        self._zone_height = self.sz_top - self.sz_bot

        self.pitches: List[MissedCalls] = None

        self.axis = None

    def plot(self, pitches: List[MissedCalls], plot: bool = True):
        """
        Plots a list of pitches using matplot lib. Input is a list of
        pitches so that multiple pitches can be printed

        Arg:
            pitches (List[PlayEvents]): List of pitches
                (game.PlayEvents) that want to be plotted
            plot (bool, optional): Argument to turn off plot but still
                do calculations. Default = True
        """

        self.pitches: List[MissedCalls] = pitches.copy()
        # normalized strike zone
        if len(self.pitches) == 1:
            self.sz_top = self.pitches[0].sz_top
            self.sz_bot = self.pitches[0].sz_bot
            self._zone_height = self.sz_top - self.sz_bot

        _, self.axis = plt.subplots()

        # creates strike zone box
        zone = patches.Rectangle((self.sX_min, self.sz_bot),
                                 width=self._PLATE_WIDTH_FEET,
                                 height=self._zone_height,
                                 facecolor='none',
                                 edgecolor='black')

        # prints strike zone box
        self.axis.add_patch(zone)

        # creates and prints each pitch in list
        for i, pitch in enumerate(self.pitches):
            pX, pZ, color = self._get_normalized_pitch_location(pitch)
            pitch = patches.Circle((pX, pZ), radius=self._BALL_RADIUS_FEET,
                                    facecolor='none', edgecolor=color)
            self.axis.add_patch(pitch)
            self.axis.text(pX, pZ, str(i+1), ha='center', va='center')

        plt.xlim(-1.5, 1.5)
        plt.ylim(1,4)
        plt.xticks([])
        plt.yticks([])
        self.axis.set_aspect('equal')

        for spine in self.axis.spines.values():
            spine.set_visible(False)

        # Able to turn off plot if used in testing
        if plot is True:
            plt.show()

    def _get_normalized_pitch_location(self, pitch: MissedCalls):
        pX = pitch.px
        pZ = pitch.pz

        code = pitch.code

        if code == 'C':
            color = 'red'
        elif code == 'B':
            color = 'green'
        else:
            color = 'black'

        # delta to top and bottom of strike zone
        d_top = pZ - pitch.sz_top
        d_bot = pZ - pitch.sz_bot

        # new pitch location accounted for normalized strike zone
        pZ_top = d_top + self.sz_top
        pZ_bot = d_bot + self.sz_bot

        if abs(d_top) > abs(d_bot):
            pZ = pZ_bot
        else:
            pZ = pZ_top

        return (pX, pZ, color)
