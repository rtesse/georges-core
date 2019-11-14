"""
TODO
"""
from typing import Dict, Callable, Tuple, Any, List, AnyStr
import os
from .. import ureg as _ureg
from ..sequences import Element
import pandas as _pd
import georges.bdsim
from ..kinematics import Kinematics as _Kinematics


BDSIM_TYPE_CODES_ORIGINAL = {
    "drift": (lambda _: Element.Drift(name=_.name, L=float(_["LENGTH"]) * _ureg.m)),
    'quadrupole': (lambda _: Element.Quadrupole(name=_.name, L=float(_["LENGTH"]) * _ureg.m, K1=_["K1"] * _ureg.m**-2)),
    "rcol": (lambda _: Element.RectangularCollimator(name=_.name)),
    "ecol": (lambda _: Element.RectangularCollimator(name=_.name)),
    "dump": (lambda _: Element.RectangularCollimator(name=_.name)),
    # "sbend": (lambda _: Element.SBend(B=float(_[2]) * _ureg.tesla, L=float(_[1]) * _ureg.m, N=float(_[3]))),
}


def load_bdsim_input_file(filename: str, path: str = '.',
                          columns: List = None,
                          with_units: bool = True,
                          ) -> _pd.DataFrame:

    _: _pd.DataFrame = georges.bdsim.BDSimOutput(os.path.join(path, filename)).model.df

    for c in _.columns:
        try:
            _[c] = _[c].apply(float)
        except ValueError:
            pass

    if with_units:
        """
        TODO
        """
        pass
        #_['LENGTH'] = _['LENGTH'].apply(lambda e: e * _ureg.m)
        #_['E1'] = _['E1'].apply(lambda e: e * _ureg.radian)
        #_['APERTURE1'] = _['APERTURE1'].apply(lambda e: e * _ureg.radian)
        #_['E2'] = _['E2'].apply(lambda e: e * _ureg.radian)
        #_['ANGLE'] = _['ANGLE'].apply(lambda e: e * _ureg.radian)
        # _['K1L'] = _['K1L'].apply(lambda e: e / _ureg.m)
        # _['TILT'] = _['TILT'].apply(lambda e: e * _ureg.radian)
    return _


def bdsim_element_factory(element: _pd.Series):
        _ = BDSIM_TYPE_CODES_ORIGINAL[element["TYPE"]]
        return _(element)
