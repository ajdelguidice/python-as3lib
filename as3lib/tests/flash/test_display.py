from as3lib import null
from as3lib.tests import as3libTestCase, TestNotImplemented
from as3lib.flash.display import MovieClip


class MovieClipTests(as3libTestCase):
    def test_addFrameScript(self):
        raise TestNotImplemented

    def test_child_property(self):
        raise TestNotImplemented

    def test_constructor(self):
        def assert_frame_labels(labels_list, check):
            if not len(check):
                self.assertEqual(labels_list.length, 0)
            else:
                for i in range(labels_list.length):
                    self.assertEqual(labels_list[i].frame, check[i][0])
                    self.assertEqual(labels_list[i].name, check[i][1])

        def assert_scene(scene, check_name, check_numFrames, check_FrameLabels):
            self.assertEqual(scene.name, check_name)
            self.assertEqual(scene.numFrames, check_numFrames)
            assert_frame_labels(scene.labels, check_FrameLabels)

        def assert_scenes(scenes, check):
            for i in range(scenes.length):
                assert_scene(scenes[i], *check[i])

        mvclip = MovieClip()
        self.assertEqual(mvclip.currentFrame, 0)
        self.assertEqual(mvclip.currentFrameLabel, null)
        self.assertEqual(mvclip.currentLabel, null)
        self.assertArray(mvclip.currentLabels, [], 0)
        assert_scene(mvclip.currentScene, '', 1, [])
        self.assertEqual(mvclip.framesLoaded, 1)
        self.assertFalse(mvclip.isPlaying)
        assert_scenes(mvclip.scenes, [['', 1, []]])
        self.assertEqual(mvclip.totalFrames, 1)

    def test_currentLabels(self):
        raise TestNotImplemented

    def test_currentLables_dupes1(self):
        raise TestNotImplemented

    def test_currentLables_dupes2(self):
        raise TestNotImplemented

    def test_currentLables_dupes3(self):
        raise TestNotImplemented

    def test_currentScene(self):
        raise TestNotImplemented

    def test_dispatchEvent(self):
        raise TestNotImplemented

    def test_dispatchEvent_cancel(self):
        raise TestNotImplemented

    def test_dispatchEvent_handlerorder(self):
        raise TestNotImplemented

    def test_dispatchEvent_selfadd(self):
        raise TestNotImplemented

    def test_dispatchEvent_target(self):
        raise TestNotImplemented

    def test_displayevents(self):
        raise TestNotImplemented

    def test_displayevents_clickgoto1(self):
        raise TestNotImplemented

    def test_displayevents_clickgoto2(self):
        raise TestNotImplemented

    def test_displayevents_clickplay(self):
        raise TestNotImplemented

    def test_displayevents_clicksymbol(self):
        raise TestNotImplemented

    def test_displayevents_constructframegoto(self):
        raise TestNotImplemented

    def test_displayevents_constructframeplay(self):
        raise TestNotImplemented

    def test_displayevents_constructframesymbol(self):
        raise TestNotImplemented

    def test_displayevents_dblhandler(self):
        raise TestNotImplemented

    def test_displayevents_enterframeplay(self):
        raise TestNotImplemented

    def test_displayevents_enterframesymbol(self):
        raise TestNotImplemented

    def test_displayevents_exitframegoto(self):
        raise TestNotImplemented

    def test_displayevents_exitframeplay(self):
        raise TestNotImplemented

    def test_displayevents_exitframesymbol(self):
        raise TestNotImplemented

    def test_displayevents_looping(self):
        raise TestNotImplemented

    def test_displayevents_stopped(self):
        raise TestNotImplemented

    def test_displayevents_swap(self):
        raise TestNotImplemented

    def test_displayevents_timeline(self):
        raise TestNotImplemented

    def test_drawrect(self):
        raise TestNotImplemented

    def test_frameconstruct_skipped(self):
        raise TestNotImplemented

    def test_goto_during_frame_script(self):
        raise TestNotImplemented

    def test_goto_overwrite(self):
        raise TestNotImplemented

    def test_goto_scene_last_frame_init(self):
        raise TestNotImplemented

    def test_goto_scene_last_frame_label(self):
        raise TestNotImplemented

    def test_gotoandplay(self):
        raise TestNotImplemented

    def test_gotoandstop(self):
        raise TestNotImplemented

    def test_gotoandstop_children(self):
        raise TestNotImplemented

    def test_gotoandstop_framescripts_self(self):
        raise TestNotImplemented

    def test_gotoandstop_framescripts1(self):
        raise TestNotImplemented

    def test_gotoandstop_framescripts2(self):
        raise TestNotImplemented

    def test_gotoandstop_queueing(self):
        raise TestNotImplemented

    def test_hittest(self):
        raise TestNotImplemented

    def test_next_frame(self):
        raise TestNotImplemented

    def test_nextscene(self):
        raise TestNotImplemented

    def test_play(self):
        raise TestNotImplemented

    def test_prev_frame(self):
        raise TestNotImplemented

    def test_prev_scene(self):
        raise TestNotImplemented

    def test_properties(self):
        raise TestNotImplemented

    def test_queued_noop_goto_swf9(self):
        raise TestNotImplemented

    def test_queued_noop_goto_swf10(self):
        raise TestNotImplemented

    def test_scenes(self):
        raise TestNotImplemented

    def test_soundtransform(self):
        raise TestNotImplemented

    def test_stop(self):
        raise TestNotImplemented

    def test_super_is_symbol(self):
        raise TestNotImplemented

    def test_symbol_constructor(self):
        raise TestNotImplemented

    def test_text_mousedown(self):
        raise TestNotImplemented

    def test_willTrigger(self):
        raise TestNotImplemented


class SpriteTests(as3libTestCase):
    ...


class StageTests(as3libTestCase):
    ...
