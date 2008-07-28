""" A viewer for mlab scene. Adds a open to open up the engine.
"""

# Author: Gael Varoquaux <gael dot varoquaux at normalesup dot org> 
# Copyright (c) 2008, Enthought, Inc.
# License: BSD Style.

# Standard library imports
from os.path import join

# Enthought library imports
from enthought.tvtk.tools.ivtk import IVTK
from enthought.tvtk.pyface.api import DecoratedScene
from enthought.traits.api import Callable, List, Either
from enthought.pyface.api import ImageResource
from enthought.pyface.action.api import Action
from enthought.resource.api import resource_path

# Local imports
from enthought.mayavi.core.ui.engine_view import EngineView
from enthought.mayavi.tools.engine_manager import engine_manager
from enthought.mayavi.core.common import error

###############################################################################
# A decorated scene with an additional button.
###############################################################################
class MlabScene(DecoratedScene):
    """ Like a decorated scene, but with more buttons.
    """

    image_search_path = [join(resource_path(), 'images'), ]

    ##########################################################################
    # Non-public interface.
    ##########################################################################
    def show_engine(self):
        """ Open the engine view corresponding to the engine of the
            scene.
        """
        try:
            engine = engine_manager.find_scene_engine(self)
            return EngineView(engine=engine).edit_traits()
        except TypeError:
            error('This scene is not managed by Mayavi')

    ######################################################################
    # Trait handlers.
    ######################################################################
    def _actions_default(self):
        actions = DecoratedScene._actions_default(self)
        actions.extend([
                    Action(tooltip="View the Mayavi pipeline",
                        image=ImageResource('m2', 
                                search_path=self.image_search_path),
                        on_perform=self.show_engine,
                        ),
                        ])
        return actions


###############################################################################
# A viewer making use of the MlabScene 
###############################################################################
class MlabViewer(IVTK):
    """ A viewer window for mlab.
    """
    size=(400, 350)

    _scene_factory = Callable(MlabScene)


def viewer_factory():
    viewer = MlabViewer()
    viewer.menu_bar_manager = None
    viewer.open()
    return viewer

if __name__ == '__main__':
    from enthought.mayavi.tools.show import show
    viewer_factory()
    show()
