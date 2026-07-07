from as3lib import Boolean, int, Object


class IIMEClient:
    ...


class CompositionAttributeRange(Object):
    @property
    def converted(self):
        return self._converted

    @converted.setter
    def converted(self, value):
        self._converted = Boolean(value)

    @property
    def relativeEnd(self):
        return self._relativeEnd

    @relativeEnd.setter
    def relativeEnd(self, value):
        self._relativeEnd = int(value)

    @property
    def relativeStart(self):
        return self._relativeStart

    @relativeStart.setter
    def relativeStart(self, value):
        self._relativeStart = int(value)

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value):
        self._selected = Boolean(value)

    def __init__(self, relativeStart: int, relativeEnd, selected: Boolean,
                 converted: Boolean):
        self.relativeStart = relativeStart
        self.relativeEnd = relativeEnd
        self.selected = selected
        self.converted = converted
