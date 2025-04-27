from __future__ import annotations

from abc import ABC, abstractmethod

from common.gui.widget.base_widget import BaseWidget


class BaseController(ABC):
    _widget: BaseWidget
    _caller: BaseController

    def __init__(self, caller: BaseController | None = None) -> None:
        self._caller = caller
        self._widget = self._get_widget_instance()

    @abstractmethod
    def _get_widget_instance(self) -> BaseWidget:
        raise NotImplementedError()

    def show(self) -> None:
        self._widget.show()
