from as3lib import false, NaN, null, Number, Object, String, true, undefined
from as3lib.flash.display import MovieClip
from as3lib.flash.events import Event, EventDispatcher, IEventDispatcher
from as3lib.tests import as3libTestCase, MethodNotImplemented, TestNotImplemented


class EventTests(as3libTestCase):
    def test_bubbles(self):
        e = Event('test_event')
        self.assertEqual(e.bubbles, false)

        e = Event('test_event', true, true)
        self.assertEqual(e.bubbles, true)

    def test_cancelable(self):
        e = Event('test_event')
        self.assertEqual(e.cancelable, false)

        e = Event('test_event', true, true)
        self.assertEqual(e.cancelable, true)

    def test_clone(self):
        # (DynEvent is a dynamic subclass of Event that fails to override clone)
        class DynEvent(Event):
            def __init__(self, type, bubbles=false, cancelable=false):
                super().__init__(type, bubbles, cancelable)

        e = DynEvent('test_event', false, true)
        e.expando = 'Original expando property!'
        self.assertEqual(e.expando, 'Original expando property!')

        e2 = e.clone()
        self.assertNotStrictEQ(e2, e)
        self.assertFalse(e2.hasOwnProperty('expando'))
        self.assertEqual(e2.type, 'test_event')
        self.assertEqual(e2.bubbles, false)
        self.assertEqual(e2.cancelable, true)
        self.assertTrue(isinstance(e2, Event))
        self.assertFalse(isinstance(e2, DynEvent))

    def test_clone_error_redispatch(self):
        raise TestNotImplemented

    def test_clone_on_redispatch(self):
        class CustomEvent(Event):
            def __init__(this, type, bubbles, cancelable):
                super().__init__(type, bubbles, cancelable)

            def clone(this):
                self.handlerCallOrder += 'C'
                return CustomEvent(this.type, this.bubbles, this.cancelable)

        self.handlerCallOrder = ''
        event = CustomEvent('custom', false, false)

        # Recursive redispatch test.
        dispatcher1 = EventDispatcher()
        dispatcher2 = EventDispatcher()

        def func1(event):
            self.handlerCallOrder += '1'
            dispatcher2.dispatchEvent(event)

        def func2(event):
            self.handlerCallOrder += '2'

        dispatcher1.addEventListener('custom', func1)

        dispatcher2.addEventListener('custom', func2)

        dispatcher1.dispatchEvent(event)

        self.assertEqual(self.handlerCallOrder, '1C2')

        # Non-recursive redispatch test.
        self.handlerCallOrder = ''
        dispatcher3 = EventDispatcher()
        dispatcher4 = EventDispatcher()

        def func3(event):
            self.handlerCallOrder += '3'

        def func4(event):
            self.handlerCallOrder += '4'

        dispatcher3.addEventListener('custom', func3)

        dispatcher4.addEventListener('custom', func4)

        event = CustomEvent('custom', false, false)

        dispatcher3.dispatchEvent(event)
        dispatcher4.dispatchEvent(event)

        self.assertEqual(self.handlerCallOrder, '3C4')

        # Event dispatched flag should not be set if the dispatcher did not have an event listener.
        # dispatcher without handler should not cause a clone
        self.handlerCallOrder = ''
        dispatcherWithoutHandler = EventDispatcher()
        dispatcherWithHandler = EventDispatcher()

        def func5(event):
            self.handlerCallOrder += '5'

        dispatcherWithHandler.addEventListener('custom', func5)

        event = CustomEvent('custom', false, false)

        dispatcherWithoutHandler.dispatchEvent(event)
        dispatcherWithHandler.dispatchEvent(event)

        self.assertEqual(self.handlerCallOrder, '5')

        del self.handlerCallOrder

    def test_formattostring(self):
        # TODO: Requires proper Object variable access
        # (DynEvent is a dynamic subclass of Event)
        class DynEvent(Event):
            def __init__(self, type, bubbles=false, cancelable=false):
                super().__init__(type, bubbles, cancelable)
                self.__evil = 0

            @property
            def evilProp(self):
                x = self.__evil
                self.__evil += 1
                return x

            @property
            def strProp(self):
                return 'strProp'

            @property
            def numProp(self):
                return 5

        e = DynEvent("test_event", false, true)
        self.assertEqual(e.formatToString('MyClass'), '[MyClass]')

        e.property = String('value')
        self.assertEqual(e.formatToString('MyClass', 'property'), '[MyClass property="value"]')

        e[2] = String('property')
        e.three = true
        e.four = Number(0.5)
        e.five = Number(10)
        e.six = NaN

        self.assertEqual(e.formatToString('MyClass', 2), '[MyClass 2="property"]')
        self.assertEqual(e.formatToString('MyClass', 2, 'property'), '[MyClass 2="property" property="value"]')
        self.assertEqual(e.formatToString('MyClass', 'property', 2, 'property'), '[MyClass property="value" 2="property" property="value"]')
        self.assertEqual(e.formatToString('MyClass', 'three', 'four', 'five'), '[MyClass three=true four=0.5 five=10]')
        self.assertEqual(e.formatToString('MyClass', 'strProp', 'numProp'), '[MyClass strProp="strProp" numProp=5]')
        self.assertEqual(e.formatToString('MyClass', 'evilProp', 2, 'evilProp'), '[MyClass evilProp=0 2="property" evilProp=1]')
        self.assertEqual(e.formatToString('MyClass', undefined), '[MyClass null=undefined]')
        self.assertEqual(e.formatToString('MyClass', null), '[MyClass null=undefined]')

        raise MethodNotImplemented('prototype')

        DynEvent.prototype.protoProp = "protoValue"

        self.assertEqual(e.formatToString('MyClass', 'protoProp'), '[MyClass protoProp="protoValue"]')

    def test_handler_exception(self):
        raise TestNotImplemented

    def test_isdefaultprevented(self):
        e = Event('test_event', false, false)
        self.assertFalse(e.isDefaultPrevented())

        e.preventDefault()
        self.assertFalse(e.isDefaultPrevented())

        e = Event('test_event', true, true)
        self.assertFalse(e.isDefaultPrevented())

        e.preventDefault()
        self.assertTrue(e.isDefaultPrevented())

    def test_target_getter(self):
        class E1(Event):
            @property
            def target(self):
                self._timesGetTarget += 1
                return self.dobj

            def __init__(self, type, dobj):
                super().__init__(type, false, false)
                self.dobj = dobj
                self._timesGetTarget = 0
                self._timesCloned = 0

            def clone(self):
                self._timesCloned += 1
                return E1(self.type, self._dobj)

        class E2(Event):
            @property
            def target(self):
                self._timesGetTarge += 1
                if self.ready:
                    return self.dobj
                self.ready = true
                return null

            def __init__(self, type, d):  # NOTE: This is how it was originally
                super().__init__(type, false, false)
                self.ready = false
                self.dobj = dobj
                self._timesGetTarget = 0
                self._timesCloned = 0

            def clone(self):
                self._timesCloned += 1
                return E2(self.type, self.dobj)

        d = MovieClip()

        # testing trivial getter
        e1 = E1('e1', d)
        d.dispatchEvent(e1)
        self.assertEqual(e1._timesGetTarget, 1)
        self.assertEqual(e1._timesCloned, 1)

        # testing 1-cycle-delayed getter
        e2 = E2('e2', d)
        d.dispatchEvent(e2)
        self.assertEqual(e1._timesGetTarget, 1)
        self.assertEqual(e1._timesCloned, 0)

    def test_target_set(self):
        event = Event('custom', false, false)
        dispatcher = EventDispatcher()
        self.eventReturn = 0

        # Before dispatch 1
        self.assertIs(event.target, null)
        self.assertIs(event.currentTarget, null)

        dispatcher.dispatchEvent(event)

        # After dispatch 1
        self.assertIs(event.target, null)
        self.assertIs(event.currentTarget, null)

        def eventFunction(event):
            self.eventReturn += 1

        dispatcher.addEventListener('custom', eventFunction)

        # Before dispatch 2
        self.assertIs(event.target, null)
        self.assertIs(event.currentTarget, null)

        dispatcher.dispatchEvent(event)

        assert self.eventReturn == 1

        # After dispatch 2
        # TODO: Check if these asserts are correct
        self.assertIs(event.target, dispatcher)
        self.assertIs(event.currentTarget, dispatcher)

        del self.eventReturn

    def test_type(self):
        e = Event('test_event')
        self.assertEqual(e.type, 'test_event')

    def test_valueof_tostring(self):
        e = Event('test_event')
        self.assertEqual(e.toString(), '[Event type="test_event" bubbles=false cancelable=false eventPhase=2]')

        raise MethodNotImplemented('prototype')
        #trace(Object.prototype.valueOf.call(e))
        # [Event type="test_event" bubbles=false cancelable=false eventPhase=2]

        self.assertTrue(type(Object.prototype.valueOf.call(e)) is Event)
        self.assertEqual(Object.prototype.toString.call(e), '[object Event]')

        e = Event("test_event", true, true)
        self.assertEqual(e.toString(), '[Event type="test_event" bubbles=true cancelable=true eventPhase=2]')
        #trace(Object.prototype.valueOf.call(e))
        # [Event type="test_event" bubbles=true cancelable=true eventPhase=2]
        self.assertTrue(type(Object.prototype.valueOf.call(e)) is Event)
        self.assertEqual(Object.prototype.toString.call(e), '[object Event]')


class EventDispatcherTests(as3libTestCase):
    def test_dispatchevent(self):
        self.eventProperties = []

        def introspect_event(event: Event):
            self.eventProperties = [event.type, event.eventPhase, event.target, event.currentTarget]

        evtd = EventDispatcher()
        evtd.addEventListener('test', introspect_event, false, 0)
        evtd.dispatchEvent(Event('test'))
        self.assertEqual(self.eventProperties[0], 'test')
        self.assertEqual(self.eventProperties[1], 2)
        self.assertStrictEQ(self.eventProperties[2], evtd)
        self.assertStrictEQ(self.eventProperties[3], evtd)

        del self.eventProperties

    def test_dispatchevent_cancel(self):
        self.handleOrder = ''

        def nocancel_event(event: Event):
            self.handleOrder += '1'

        def cancel_event(event: Event):
            self.handleOrder += '2'
            event.preventDefault()

        def stop_event(event: Event):
            self.handleOrder += '3'
            event.stopPropagation()

        def stop_immediate_event(event: Event):
            self.handleOrder += '4'
            event.stopImmediatePropagation()

        evtd = EventDispatcher()

        evtd.addEventListener('test', nocancel_event, false, 0)
        self.assertTrue(evtd.dispatchEvent(Event('test', true, true)))
        self.assertEqual(self.handleOrder, '1')

        self.handleOrder = ''
        evtd.addEventListener('test', cancel_event, false, 0)
        self.assertFalse(evtd.dispatchEvent(Event('test', true, true)))
        self.assertEqual(self.handleOrder, '12')

        self.handleOrder = ''
        evtd.removeEventListener('test', cancel_event)
        evtd.addEventListener('test', stop_event, false, 5)
        self.assertTrue(evtd.dispatchEvent(Event('test', true, true)))
        self.assertEqual(self.handleOrder, '31')

        self.handleOrder = ''
        evtd.addEventListener('test', stop_immediate_event, false, 10)
        self.assertTrue(evtd.dispatchEvent(Event('test', true, true)))
        self.assertEqual(self.handleOrder, '4')

        del self.handleOrder

    def test_dispatchevent_handlerorder(self):
        self.handleOrder = ''

        def handler_one(event: Event):
            # trace("//(handler_one executed...)")
            self.handleOrder += '1'

        def handler_two(event: Event):
            # trace("//(handler_two executed...)")
            self.handleOrder += '2'

        def handler_three(event: Event):
            # trace("//(handler_three executed...)")
            self.handleOrder += '3'

        evtd = EventDispatcher()
        evtd.addEventListener('test', handler_one, false, 0)
        evtd.addEventListener('test', handler_two, false, 5)
        evtd.addEventListener('test', handler_three, false, 0)

        evtd.dispatchEvent(Event('test'))
        self.assertEqual(self.handleOrder, '213')

        self.handleOrder = ''
        evtd.removeEventListener('test', handler_two)

        evtd.dispatchEvent(Event('test'))
        self.assertEqual(self.handleOrder, '13')

        self.handleOrder = ''
        evtd.addEventListener('test', handler_two, true, 5)
        evtd.addEventListener('test2', handler_two, false, 5)

        evtd.dispatchEvent(Event('test'))
        self.assertEqual(self.handleOrder, '13')

        self.handleOrder = ''
        evtd.addEventListener('test', handler_two, false, -5)

        evtd.dispatchEvent(Event('test'))
        self.assertEqual(self.handleOrder, '132')

        del self.handleOrder

    def test_dispatchevent_indirect(self):
        raise TestNotImplemented

    def test_dispatchevent_this(self):
        raise TestNotImplemented

    def test_haseventlistener(self):
        evtd = EventDispatcher()
        self.listenerCalled = 0

        def listener(e):
            self.listenerCalled += 1

        self.assertFalse(evtd.hasEventListener('test'))

        evtd.addEventListener('test', listener, false, 0)
        self.assertTrue(evtd.hasEventListener('test'))

        evtd.removeEventListener('test', listener, false)
        self.assertFalse(evtd.hasEventListener('test'))

        evtd.removeEventListener('test', listener, false)
        self.assertFalse(evtd.hasEventListener('test'))

        evtd.addEventListener('test', listener, false, 0)
        self.assertTrue(evtd.hasEventListener('test'))

        evtd.addEventListener('test', listener, false, 0)
        self.assertTrue(evtd.hasEventListener('test'))

        evtd.removeEventListener('test', listener, false)
        self.assertFalse(evtd.hasEventListener('test'))

        evtd.removeEventListener('test', listener, false)
        self.assertFalse(evtd.hasEventListener('test'))

        self.assertEqual(self.listenerCalled, 0)
        del self.listenerCalled

    def test_interface_invoke(self):
        self.dispatched = False

        def invokeDispatcher(dispatcher: IEventDispatcher):
            # This method is invoked on the interface, not a concrete class
            dispatcher.dispatchEvent(Event("myEvent"))
            self.dispatched = True

        invokeDispatcher(MovieClip())
        self.assertTrue(self.dispatched)
        del self.dispatched

    def test_tostring(self):
        ed = EventDispatcher()
        self.assertEqual(ed.toString(), '[object EventDispatcher]')

        class CustomDispatch(EventDispatcher):
            def toString(self):
                return super().toString()

        cust = CustomDispatch()
        self.assertEqual(cust.toString(), '[object CustomDispatch]')

    def test_willtrigger(self):
        evtd = EventDispatcher()
        self.listenerCalled = 0

        def listener(event):
            self.listenerCalled += 1

        self.assertFalse(evtd.willTrigger('test'))

        evtd.addEventListener('test', listener, false, 0)
        self.assertTrue(evtd.willTrigger('test'))

        evtd.removeEventListener('test', listener, false)
        self.assertFalse(evtd.willTrigger('test'))

        evtd.removeEventListener('test', listener, false)
        self.assertFalse(evtd.willTrigger('test'))

        evtd.addEventListener('test', listener, false, 0)
        self.assertTrue(evtd.willTrigger('test'))

        evtd.addEventListener('test', listener, false, 0)
        self.assertTrue(evtd.willTrigger('test'))

        evtd.removeEventListener('test', listener, false)
        self.assertFalse(evtd.willTrigger('test'))

        evtd.removeEventListener('test', listener, false)
        self.assertFalse(evtd.willTrigger('test'))

        self.assertEqual(self.listenerCalled, 0)
        del self.listenerCalled


class MouseEventTests(as3libTestCase):
    def test_constructor(self):
        raise TestNotImplemented

    def test_stagexy(self):
        raise TestNotImplemented

    def test_valueOf(self):
        raise TestNotImplemented

    def test_toString(self):
        raise TestNotImplemented
