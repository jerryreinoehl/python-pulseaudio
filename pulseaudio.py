from ctypes import *

import sys


try:
    libpulse = cdll.LoadLibrary("libpulse.so")
except Exception as e:
    exit(e)


# defines
PA_CHANNELS_MAX = 32


# pa_volume
PA_VOLUME_T = c_uint32
PA_VOLUME_NORM = 65536
PA_VOLUME_MUTED = 0


# enum pa_context_state
PA_CONTEXT_STATE_T = c_int
PA_CONTEXT_UNCONNECTED = 0x0
PA_CONTEXT_CONNECTING = 0x1
PA_CONTEXT_AUTHORIZING = 0x2
PA_CONTEXT_SETTING_NAME = 0x3
PA_CONTEXT_READY = 0x4
PA_CONTEXT_FAILED = 0x5
PA_CONTEXT_TERMINATED = 0x6


# enum pa_context_flags
PA_CONTEXT_FLAGS_T = c_int
PA_CONTEXT_NOFLAGS = 0x0
PA_CONTEXT_NOAUTOSPAWN = 0x1
PA_CONTEXT_NOFAIL = 0x2


# enum pa_operation_state
PA_OPERATION_STATE_T = c_int
PA_OPERATION_RUNNING = 0x0
PA_OPERATION_DONE = 0x1
PA_OPERATION_CANCELLED = 0x2


# enum pa_subscription_mask
PA_SUBSCRIPTION_MASK_T = c_int
PA_SUBSCRIPTION_MASK_NULL = 0x0
PA_SUBSCRIPTION_MASK_SINK = 0x1
PA_SUBSCRIPTION_MASK_SOURCE = 0x2
PA_SUBSCRIPTION_MASK_SINK_INPUT = 0x4
PA_SUBSCRIPTION_MASK_SOURCE_OUTPUT = 0x8
PA_SUBSCRIPTION_MASK_MODULE = 0x10
PA_SUBSCRIPTION_MASK_CLIENT = 0x20
PA_SUBSCRIPTION_MASK_SAMPLE_CACHE = 0x40
PA_SUBSCRIPTION_MASK_SERVER = 0x80
PA_SUBSCRIPTION_MASK_AUTOLOAD = 0x100
PA_SUBSCRIPTION_MASK_CARD = 0x200
PA_SUBSCRIPTION_MASK_ALL = 0x2FF


# enum pa_subscription_event_type
PA_SUBSCRIPTION_EVENT_T = c_int
PA_SUBSCRIPTION_EVENT_SINK = 0x0
PA_SUBSCRIPTION_EVENT_SOURCE = 0x1
PA_SUBSCRIPTION_EVENT_SINK_INPUT = 0x2
PA_SUBSCRIPTION_EVENT_SOURCE_OUTPUT = 0x3
PA_SUBSCRIPTION_EVENT_MODULE = 0x4
PA_SUBSCRIPTION_EVENT_CLIENT = 0x5
PA_SUBSCRIPTION_EVENT_SAMPLE_CACHE = 0x6
PA_SUBSCRIPTION_EVENT_SERVER = 0x7
PA_SUBSCRIPTION_EVENT_AUTOLOAD = 0x8
PA_SUBSCRIPTION_EVENT_CARD = 0x9
PA_SUBSCRIPTION_EVENT_FACILITY_MASK = 0xF
PA_SUBSCRIPTION_EVENT_NEW = 0x0
PA_SUBSCRIPTION_EVENT_CHANGE = 0x10
PA_SUBSCRIPTION_EVENT_REMOVE = 0x20
PA_SUBSCRIPTION_EVENT_TYPE_MASK = 0x30


# enum pa_sink_state
PA_SINK_STATE_T = c_int
PA_SINK_INVALID_STATE = -1
PA_SINK_RUNNING = 0
PA_SINK_IDLE = 1
PA_SINK_SUSPENDED = 2


PA_USEC_T = c_uint64


class Struct(Structure):
    pass


PA_CONTEXT = Struct
PA_FORMAT_INFO = Struct
PA_MAINLOOP_API = Struct
PA_MAINLOOP = Struct
PA_OPERATION = Struct
PA_PORT_INFO = Struct
PA_PROPLIST = Struct
PA_SPAWN_API = Struct
PA_THREADED_MAINLOOP = Struct


class PA_CVOLUME(Structure):
    _fields_ = [
        ("channels", c_uint8),
        ("values", PA_VOLUME_T * PA_CHANNELS_MAX)
    ]


class PA_SAMPLE_SPEC(Structure):
    _fields_ = [
        ("format", c_int),
        ("rate", c_uint32),
        ("channels", c_uint32),
    ]


class PA_CHANNEL_MAP(Structure):
    _fields_ = [
        ("channels", c_uint8),
        ("map", c_int * PA_CHANNELS_MAX),
    ]


class PA_SINK_INFO(Structure):
    _fields_ = [
        ("name", c_char_p),
        ("index", c_uint32),
        ("description", c_char_p),
        ("sample_spec", PA_SAMPLE_SPEC),
        ("channel_map", PA_CHANNEL_MAP),
        ("owner_module", c_uint32),
        ("volume", PA_CVOLUME),
        ("mute", c_int),
        ("monitor_source", c_uint32),
        ("monitor_source_name", c_char_p),
        ("latency", PA_USEC_T),
        ("driver", c_char_p),
        ("flags", c_int),
        ("proplist", POINTER(PA_PROPLIST)),
        ("configured_latency", PA_USEC_T),
        ("base_volume", c_int),
        ("state", c_int),
        ("n_volume_steps", c_int),
        ("card", c_uint32),
        ("n_ports", c_uint32),
        ("ports", POINTER(POINTER(PA_PORT_INFO))),
        ("active_port", POINTER(PA_PORT_INFO)),
        ("n_formats", c_uint8),
        ("formats", POINTER(POINTER(PA_FORMAT_INFO))),
    ]


class PA_SERVER_INFO(Structure):
    _fields_ = [
        ("user_name", c_char_p),
        ("host_name", c_char_p),
        ("server_version", c_char_p),
        ("server_name", c_char_p),
        ("sample_spec", PA_SAMPLE_SPEC),
        ("default_sink_name", c_char_p),
        ("default_source_name", c_char_p),
        ("cookie", c_uint32),
        ("channel_map", PA_CHANNEL_MAP),
    ]


PA_SINK_INFO_CB_T = CFUNCTYPE(
    None, POINTER(PA_CONTEXT), POINTER(PA_SINK_INFO), c_int, c_void_p
)


PA_CONTEXT_SUCCESS_CB_T = CFUNCTYPE(None, POINTER(PA_CONTEXT), c_int, c_void_p)


PA_CONTEXT_SUBSCRIBE_CB_T = CFUNCTYPE(
    None, POINTER(PA_CONTEXT), c_int, c_uint32, c_void_p
)


PA_CONTEXT_NOTIFY_CB_T = CFUNCTYPE(
    None, POINTER(PA_CONTEXT), c_void_p
)


PA_SERVER_INFO_CB_T = CFUNCTYPE(
    None, POINTER(PA_CONTEXT), POINTER(PA_SERVER_INFO), c_void_p
)


# pa_mainloop
pa_mainloop_new = libpulse.pa_mainloop_new
pa_mainloop_new.restype = POINTER(PA_MAINLOOP)
pa_mainloop_new.argtypes = []


pa_mainloop_free = libpulse.pa_mainloop_free
pa_mainloop_free.restype = None
pa_mainloop_free.argtypes = [POINTER(PA_MAINLOOP)]


pa_mainloop_get_api = libpulse.pa_mainloop_get_api
pa_mainloop_get_api.restype = POINTER(PA_MAINLOOP_API)
pa_mainloop_get_api.argtypes = [POINTER(PA_MAINLOOP)]


pa_mainloop_iterate = libpulse.pa_mainloop_iterate
pa_mainloop_iterate.restype = c_int
pa_mainloop_iterate.argtypes = [POINTER(PA_MAINLOOP), c_int, POINTER(c_int)]


pa_mainloop_prepare = libpulse.pa_mainloop_prepare
pa_mainloop_prepare.restype = c_int
pa_mainloop_prepare.argtypes = [POINTER(PA_MAINLOOP), c_int]


pa_mainloop_poll = libpulse.pa_mainloop_poll
pa_mainloop_poll.restype = c_int
pa_mainloop_poll.argtypes = [POINTER(PA_MAINLOOP)]


pa_mainloop_dispatch = libpulse.pa_mainloop_dispatch
pa_mainloop_dispatch.restype = c_int
pa_mainloop_dispatch.argtypes = [POINTER(PA_MAINLOOP)]


pa_mainloop_run = libpulse.pa_mainloop_run
pa_mainloop_run.restype = c_int
pa_mainloop_run.argtypes = [POINTER(PA_MAINLOOP), POINTER(c_int)]


pa_mainloop_quit = libpulse.pa_mainloop_quit
pa_mainloop_quit.restype = None
pa_mainloop_quit.argtypes = [POINTER(PA_MAINLOOP), c_int]


pa_mainloop_wakeup = libpulse.pa_mainloop_wakeup
pa_mainloop_wakeup.restype = None
pa_mainloop_wakeup.argtypes = [POINTER(PA_MAINLOOP)]


pa_mainloop_get_retval = libpulse.pa_mainloop_get_retval
pa_mainloop_get_retval.restype = c_int
pa_mainloop_get_retval.argtypes = [POINTER(PA_MAINLOOP)]


# pa_threaded_mainloop
pa_threaded_mainloop_new = libpulse.pa_threaded_mainloop_new
pa_threaded_mainloop_new.restype = POINTER(PA_THREADED_MAINLOOP)
pa_threaded_mainloop_new.argtypes = []


pa_threaded_mainloop_free = libpulse.pa_threaded_mainloop_free
pa_threaded_mainloop_free.restype = None
pa_threaded_mainloop_free.argtypes = [POINTER(PA_THREADED_MAINLOOP)]


pa_threaded_mainloop_get_api = libpulse.pa_threaded_mainloop_get_api
pa_threaded_mainloop_get_api.restype = POINTER(PA_MAINLOOP_API)
pa_threaded_mainloop_get_api.argtypes = [
    POINTER(PA_THREADED_MAINLOOP)
]


pa_threaded_mainloop_set_name = libpulse.pa_threaded_mainloop_set_name
pa_threaded_mainloop_set_name.restype = None
pa_threaded_mainloop_set_name.argtypes = [
    POINTER(PA_THREADED_MAINLOOP), c_char_p
]


pa_threaded_mainloop_signal = libpulse.pa_threaded_mainloop_signal
pa_threaded_mainloop_signal.restype = None
pa_threaded_mainloop_signal.argtypes = [
    POINTER(PA_THREADED_MAINLOOP), c_int
]


pa_threaded_mainloop_accept = libpulse.pa_threaded_mainloop_accept
pa_threaded_mainloop_accept.restype = None
pa_threaded_mainloop_accept.argtypes = [POINTER(PA_THREADED_MAINLOOP)]


pa_threaded_mainloop_start = libpulse.pa_threaded_mainloop_start
pa_threaded_mainloop_start.restype = c_int
pa_threaded_mainloop_start.argtypes = [POINTER(PA_THREADED_MAINLOOP)]


pa_threaded_mainloop_stop = libpulse.pa_threaded_mainloop_stop
pa_threaded_mainloop_stop.restype = None
pa_threaded_mainloop_stop.argtypes = [POINTER(PA_THREADED_MAINLOOP)]


pa_threaded_mainloop_lock = libpulse.pa_threaded_mainloop_lock
pa_threaded_mainloop_lock.restype = None
pa_threaded_mainloop_lock.argtypes = [POINTER(PA_THREADED_MAINLOOP)]


pa_threaded_mainloop_unlock = libpulse.pa_threaded_mainloop_unlock
pa_threaded_mainloop_unlock.restype = None
pa_threaded_mainloop_unlock.argtypes = [POINTER(PA_THREADED_MAINLOOP)]


pa_threaded_mainloop_wait = libpulse.pa_threaded_mainloop_wait
pa_threaded_mainloop_wait.restype = None
pa_threaded_mainloop_wait.argtypes = [POINTER(PA_THREADED_MAINLOOP)]


pa_threaded_mainloop_get_retval = libpulse.pa_threaded_mainloop_get_retval
pa_threaded_mainloop_get_retval.restype = c_int
pa_threaded_mainloop_get_retval.argtypes = [
    POINTER(PA_THREADED_MAINLOOP)
]


pa_threaded_mainloop_in_thread = libpulse.pa_threaded_mainloop_in_thread
pa_threaded_mainloop_in_thread.restype = c_int
pa_threaded_mainloop_in_thread.argtypes = [
    POINTER(PA_THREADED_MAINLOOP)
]


# pa_cvolume
pa_cvolume_avg = libpulse.pa_cvolume_avg
pa_cvolume_avg.restype = PA_VOLUME_T
pa_cvolume_avg.argtypes = [POINTER(PA_CVOLUME)]


pa_cvolume_set = libpulse.pa_cvolume_set
pa_cvolume_set.restype = POINTER(PA_CVOLUME)
pa_cvolume_set.argtypes = [POINTER(PA_CVOLUME), c_uint, PA_VOLUME_T]


pa_cvolume_dec = libpulse.pa_cvolume_dec
pa_cvolume_dec.restype = POINTER(PA_CVOLUME)
pa_cvolume_dec.argtypes = [POINTER(PA_CVOLUME), PA_VOLUME_T]


pa_cvolume_inc = libpulse.pa_cvolume_inc
pa_cvolume_inc.restype = POINTER(PA_CVOLUME)
pa_cvolume_inc.argtypes = [POINTER(PA_CVOLUME), PA_VOLUME_T]


pa_cvolume_inc_clamp = libpulse.pa_cvolume_inc_clamp
pa_cvolume_inc_clamp.restype = POINTER(PA_CVOLUME)
pa_cvolume_inc_clamp.argtypes = [POINTER(PA_CVOLUME), PA_VOLUME_T, PA_VOLUME_T]


pa_cvolume_snprint = libpulse.pa_cvolume_snprint
pa_cvolume_snprint.restype = c_char_p
pa_cvolume_snprint.argtypes = [c_char_p, c_uint, POINTER(PA_CVOLUME)]


pa_sw_cvolume_snprint_dB = libpulse.pa_sw_cvolume_snprint_dB
pa_sw_cvolume_snprint_dB.restype = c_char_p
pa_sw_cvolume_snprint_dB.argtypes = [
    c_char_p, c_uint, POINTER(PA_CVOLUME)
]


# pa_context
pa_context_new = libpulse.pa_context_new
pa_context_new.restype = POINTER(PA_CONTEXT)
pa_context_new.argtypes = [POINTER(PA_MAINLOOP_API), c_char_p]


pa_context_connect = libpulse.pa_context_connect
pa_context_connect.restype = c_int
pa_context_connect.argtypes = [
    POINTER(PA_CONTEXT), c_char_p, PA_CONTEXT_FLAGS_T, POINTER(PA_SPAWN_API)
]


pa_context_disconnect = libpulse.pa_context_disconnect
pa_context_disconnect.restype = None
pa_context_disconnect.argtypes = [POINTER(PA_CONTEXT)]


pa_context_errno = libpulse.pa_context_errno
pa_context_errno.restype = c_int
pa_context_errno.argtypes = [POINTER(PA_CONTEXT)]


pa_context_get_state = libpulse.pa_context_get_state
pa_context_get_state.restype = PA_CONTEXT_STATE_T
pa_context_get_state.argtypes = [POINTER(PA_CONTEXT)]


pa_context_set_sink_mute_by_index = libpulse.pa_context_set_sink_mute_by_index
pa_context_set_sink_mute_by_index.restype = POINTER(PA_OPERATION)
pa_context_set_sink_mute_by_index.argtypes = [
    POINTER(PA_CONTEXT),
    c_uint32,
    c_int,
    PA_CONTEXT_SUCCESS_CB_T,
    c_void_p,
]


pa_context_set_sink_mute_by_name = libpulse.pa_context_set_sink_mute_by_name
pa_context_set_sink_mute_by_name.restype = POINTER(PA_OPERATION)
pa_context_set_sink_mute_by_name.argtypes = [
    POINTER(PA_CONTEXT), c_char_p, c_int, PA_CONTEXT_SUCCESS_CB_T, c_void_p
]


pa_context_suspend_sink_by_name = libpulse.pa_context_suspend_sink_by_name
pa_context_suspend_sink_by_name.restype = POINTER(PA_OPERATION)
pa_context_suspend_sink_by_name.argtypes = [
    POINTER(PA_CONTEXT), c_char_p, c_int, PA_CONTEXT_SUCCESS_CB_T, c_void_p
]


pa_context_get_sink_info_by_index = libpulse.pa_context_get_sink_info_by_index
pa_context_get_sink_info_by_index.restype = POINTER(PA_OPERATION)
pa_context_get_sink_info_by_index.argtypes = [
    POINTER(PA_CONTEXT), c_uint32, PA_SINK_INFO_CB_T, c_void_p
]


pa_context_get_sink_info_by_name = libpulse.pa_context_get_sink_info_by_name
pa_context_get_sink_info_by_name.restype = POINTER(PA_OPERATION)
pa_context_get_sink_info_by_name.argtypes = [
    POINTER(PA_CONTEXT), c_char_p, PA_SINK_INFO_CB_T, c_void_p
]


pa_context_set_sink_volume_by_index = libpulse.pa_context_set_sink_volume_by_index
pa_context_set_sink_volume_by_index.restype = POINTER(PA_OPERATION)
pa_context_set_sink_volume_by_index.argtypes = [
    POINTER(PA_CONTEXT),
    c_uint32,
    POINTER(PA_CVOLUME),
    PA_CONTEXT_SUCCESS_CB_T,
    c_void_p
]


pa_context_set_sink_volume_by_name = libpulse.pa_context_set_sink_volume_by_name
pa_context_set_sink_volume_by_name.restype = POINTER(PA_OPERATION)
pa_context_set_sink_volume_by_name.argtypes = [
    POINTER(PA_CONTEXT),
    c_char_p,
    POINTER(PA_CVOLUME),
    PA_CONTEXT_SUCCESS_CB_T,
    c_void_p,
]


pa_context_set_state_callback = libpulse.pa_context_set_state_callback
pa_context_set_state_callback.restype = None
pa_context_set_state_callback.argtypes = [
    POINTER(PA_CONTEXT),
    PA_CONTEXT_NOTIFY_CB_T,
    c_void_p,
]


pa_context_set_subscribe_callback = libpulse.pa_context_set_subscribe_callback
pa_context_set_subscribe_callback.restype = None
pa_context_set_subscribe_callback.argtypes = [
    POINTER(PA_CONTEXT), PA_CONTEXT_SUBSCRIBE_CB_T, c_void_p
]


pa_context_subscribe = libpulse.pa_context_subscribe
pa_context_subscribe.restype = POINTER(PA_OPERATION)
pa_context_subscribe.argtypes = [
    POINTER(PA_CONTEXT),
    PA_SUBSCRIPTION_MASK_T,
    PA_CONTEXT_SUCCESS_CB_T,
    c_void_p
]


pa_context_get_sink_info_by_index = libpulse.pa_context_get_sink_info_by_index
pa_context_get_sink_info_by_index.restype = POINTER(PA_OPERATION)
pa_context_get_sink_info_by_index.argtypes = [
    POINTER(PA_CONTEXT), c_uint32, PA_SINK_INFO_CB_T, c_void_p
]


pa_context_get_server_info = libpulse.pa_context_get_server_info
pa_context_get_server_info.restype = POINTER(PA_OPERATION)
pa_context_get_server_info.argtypes = [
    POINTER(PA_CONTEXT), PA_SERVER_INFO_CB_T, c_void_p
]


# pa_operation
pa_operation_get_state = libpulse.pa_operation_get_state
pa_operation_get_state.restype = PA_OPERATION_STATE_T
pa_operation_get_state.argtypes = [POINTER(PA_OPERATION)]


pa_operation_unref = libpulse.pa_operation_unref
pa_operation_unref.restype = None
pa_operation_unref.argtypes = [POINTER(PA_OPERATION)]


class SinkInfo():
    def __init__(self, name, index, description, mute, volume, state):
        self.name = name
        self.index = index
        self.description = description
        self.mute = mute
        self.volume = volume
        self.state = state

    @property
    def volume_avg(self):
        """Returns the average volume of all the channels."""
        return sum(self.volume) / len(self.volume)

    @classmethod
    def from_pa_sink_info(cls, pa_sink_info: PA_SINK_INFO):
        """Creates and returns a `SinkInfo` from a `PA_SINK_INFO` object."""
        name = pa_sink_info.name.decode()
        index = pa_sink_info.index
        description = pa_sink_info.description.decode()
        mute = bool(pa_sink_info.mute)
        state = pa_sink_info.state

        channels = int(pa_sink_info.volume.channels)
        values = list(pa_sink_info.volume.values[:channels])
        base_volume = pa_sink_info.base_volume

        for i, value in enumerate(values):
            values[i] = value / base_volume

        volume = values

        return SinkInfo(name, index, description, mute, volume, state)


class ServerInfo():
    def __init__(
        self,
        user_name,
        host_name,
        server_version,
        server_name,
        default_sink_name,
        default_source_name,
        cookie,
    ):
        self.user_name = user_name
        self.host_name = host_name
        self.server_version = server_version
        self.server_name = server_name
        self.default_sink_name = default_sink_name
        self.default_source_name = default_source_name
        self.cookie = cookie

    @classmethod
    def from_pa_server_info(cls, pa_server_info: PA_SERVER_INFO):
        return ServerInfo(
            pa_server_info.user_name.decode(),
            pa_server_info.host_name.decode(),
            pa_server_info.server_version.decode(),
            pa_server_info.server_name.decode(),
            pa_server_info.default_sink_name.decode(),
            pa_server_info.default_source_name.decode(),
            int(pa_server_info.cookie),
        )


class PulseAudio():
    def __init__(self, default_sink=None, client_name=None, max_vol=1.5):
        if client_name != None:
            client_name = client_name.encode()
        else:
            client_name = sys.argv[0].encode()

        self._max_vol = max_vol
        self._sink_info = None
        self._server_info = None
        self._subscribe_cbs = []

        self._server_info_cb = PA_SERVER_INFO_CB_T(self._server_info_cb)
        self._sink_info_cb = PA_SINK_INFO_CB_T(self._sink_info_cb)
        self._notify_cb = PA_CONTEXT_NOTIFY_CB_T(self._notify_cb)
        self._success_cb = PA_CONTEXT_SUCCESS_CB_T(self._success_cb)
        self._subscribe_cb = PA_CONTEXT_SUBSCRIBE_CB_T(self._subscribe_cb)
        self._notify_all = PA_SINK_INFO_CB_T(self._notify_all)

        self._mainloop = pa_threaded_mainloop_new()
        self._mainloop_api = pa_threaded_mainloop_get_api(self._mainloop)
        self._context = pa_context_new(self._mainloop_api, client_name)

        self._start()
        self._connect()
        self._subscribe()

        if default_sink == None:
            self._set_default_sink()
        else:
            self._default_sink = default_sink.encode()

    def __del__(self):
        pa_context_disconnect(self._context)

    def _start(self):
        """Starts the mainloop."""
        pa_threaded_mainloop_lock(self._mainloop)
        pa_threaded_mainloop_start(self._mainloop)
        pa_threaded_mainloop_unlock(self._mainloop)

    def _connect(self):
        """Connects to the PulseAudio server."""
        pa_context_set_state_callback(
            self._context,
            self._notify_cb,
            None
        )

        pa_threaded_mainloop_lock(self._mainloop)
        pa_context_connect(self._context, None, PA_CONTEXT_NOFLAGS, None)
        pa_threaded_mainloop_wait(self._mainloop)
        pa_threaded_mainloop_unlock(self._mainloop)

    def _notify_cb(self, context, userdata):
        state = pa_context_get_state(context)

        if state == PA_CONTEXT_READY:
            pa_threaded_mainloop_signal(self._mainloop, 0)
        elif state == PA_CONTEXT_FAILED:
            # XXX Raise an error.
            pa_threaded_mainloop_signal(self._mainloop, 0)

    def _subscribe(self):
        """Subscribes to PulseAudio sink events. Events are handled by
        `_subscribe_cb`.
        """
        pa_context_set_subscribe_callback(
            self._context, self._subscribe_cb, None
        )

        pa_threaded_mainloop_lock(self._mainloop)

        op = pa_context_subscribe(
            self._context, PA_SUBSCRIPTION_MASK_SINK, self._success_cb, None
        )

        while pa_operation_get_state(op) == PA_OPERATION_RUNNING:
            pa_threaded_mainloop_wait(self._mainloop)

        pa_operation_unref(op)

        pa_threaded_mainloop_unlock(self._mainloop)

    def _subscribe_cb(self, context, event_type, index, userdata):
        """Handles new sink events."""
        op = pa_context_get_sink_info_by_name(
            self._context, self._default_sink, self._notify_all, None
        )

        pa_operation_unref(op)

    def _notify_all(self, context, sink_info, eol, userdata):
        """Notifies all callbacks in `_subscribe_cbs`."""
        if eol:
            return

        for cb in self._subscribe_cbs:
            cb(SinkInfo.from_pa_sink_info(sink_info.contents))

    def _success_cb(self, context, success, userdata):
        # check success and raise error
        pa_threaded_mainloop_signal(self._mainloop, 0)

    def _get_server_info(self):
        self._server_info = None

        op = pa_context_get_server_info(
            self._context, self._server_info_cb, None
        )

        while self._server_info == None:
            pa_threaded_mainloop_wait(self._mainloop)

        pa_operation_unref(op)

    def _server_info_cb(self, context, server_info, userdata):
        self._server_info = server_info
        pa_threaded_mainloop_signal(self._mainloop, 1)

    def _set_default_sink(self):
        pa_threaded_mainloop_lock(self._mainloop)

        self._get_server_info()

        self._default_sink = self._server_info.contents.default_sink_name

        pa_threaded_mainloop_accept(self._mainloop)
        pa_threaded_mainloop_unlock(self._mainloop)

    def _get_sink_info(self, sink):
        self._sink_info = None

        op = pa_context_get_sink_info_by_name(
            self._context, sink, self._sink_info_cb, None
        )

        while self._sink_info == None:
            pa_threaded_mainloop_wait(self._mainloop)

        pa_operation_unref(op)

    def _sink_info_cb(self, context, sink_info, eol, userdata):
        if eol:
            return

        self._sink_info = sink_info

        pa_threaded_mainloop_signal(self._mainloop, 1)

    @property
    def default_sink(self):
        return self._default_sink.decode()

    def set_sink_mute(self, mute: bool = None, sink: str = None):
        """Mutes or unmutes the given sink, or the default sink if not
        specified. If `mute` is `None` then toggles the mute.
        """
        sink = self._default_sink if sink == None else sink.encode()

        pa_threaded_mainloop_lock(self._mainloop)

        # toggle mute
        if mute == None:
            self._get_sink_info(sink)

            mute = not self._sink_info.contents.mute

            pa_threaded_mainloop_accept(self._mainloop)

        op = pa_context_set_sink_mute_by_name(
            self._context, sink, mute, self._success_cb, None
        )

        while pa_operation_get_state(op) == PA_OPERATION_RUNNING:
            pa_threaded_mainloop_wait(self._mainloop)

        pa_operation_unref(op)

        pa_threaded_mainloop_unlock(self._mainloop)

    def set_sink_volume(self, vol, sink: str = None):
        """Sets the volume of the given sink, or the default sink if not
        specified.
        """
        sink = self._default_sink if sink == None else sink.encode()

        pa_threaded_mainloop_lock(self._mainloop)

        self._get_sink_info(sink)

        cvolume = self._sink_info.contents.volume
        base_volume = self._sink_info.contents.base_volume

        pa_threaded_mainloop_accept(self._mainloop)

        try:
            self._set_cvolume(vol, cvolume, base_volume)
        except (TypeError, ValueError):
            pa_threaded_mainloop_unlock(self._mainloop)
            raise

        op = pa_context_set_sink_volume_by_name(
            self._context, sink, byref(cvolume), self._success_cb, None
        )

        while pa_operation_get_state(op) == PA_OPERATION_RUNNING:
            pa_threaded_mainloop_wait(self._mainloop)

        pa_operation_unref(op)

        pa_threaded_mainloop_unlock(self._mainloop)

    def _set_cvolume(self, vol, cvolume, base):
        new_vol = None

        if isinstance(vol, float):
            new_vol = int(base * vol)
        elif isinstance(vol, int):
            new_vol = vol
        elif isinstance(vol, str):
            if vol.startswith("+") and vol.endswith("%"):
                pa_cvolume_inc_clamp(
                    byref(cvolume),
                    int(base * float(vol[1:-1])/100),
                    int(base * self._max_vol),
                )
                return
            elif vol.startswith("-") and vol.endswith("%"):
                pa_cvolume_dec(
                    byref(cvolume), int(base * float(vol[1:-1])/100)
                )
                return
            elif vol.endswith("%"):
                new_vol = int(base * float(vol[:-1])/100)
            else:
                raise ValueError("Unable to determine volume: %s" % vol)
        elif isinstance(vol, list):
            self._set_cvolume_list(vol, cvolume, base)
            return
        else:
            raise TypeError("Volume unsupported type: %s" % type(vol))

        pa_cvolume_set(
            byref(cvolume), cvolume.channels, self._clamp(new_vol, base)
        )

    def suspend_sink(self, suspend: bool = None, sink: str = None):
        """Suspends or resumes the given sink, or the default sink if not
        specified. If `suspend` is `None` then the sink if resumed if the
        current sink state is `PA_SINK_SUSPENDED` and suspended otherwise.
        """
        sink = self._default_sink if sink == None else sink.encode()

        pa_threaded_mainloop_lock(self._mainloop)

        if suspend == None:
            self._get_sink_info(sink)

            sink_state = self._sink_info.contents.state
            suspend = False if sink_state == PA_SINK_SUSPENDED else True

            pa_threaded_mainloop_accept(self._mainloop)

        op = pa_context_suspend_sink_by_name(
            self._context, sink, suspend, self._success_cb, None
        )

        while pa_operation_get_state(op) == PA_OPERATION_RUNNING:
            pa_threaded_mainloop_wait(self._mainloop)

        pa_operation_unref(op)
        pa_threaded_mainloop_unlock(self._mainloop)

    def _set_cvolume_list(self, vols, cvolume, base):
        for i, vol in enumerate(vols):
            if isinstance(vol, float):
                cvolume.values[i] = int(base * vol)
            elif isinstance(vol, int):
                cvolume.values[i] = vol
            elif isinstance(vol, str):
                if vol.startswith("+") and vol.endswith("%"):
                    cvolume.values[i] += int(base * float(vol[1:-1])/100)
                elif vol.startswith("-") and vol.endswith("%"):
                    cvolume.values[i] -= int(base * float(vol[1:-1])/100)
                elif vol.endswith("%"):
                    cvolume.values[i] = int(base * float(vol[:-1])/100)
                else:
                    raise ValueError("Unable to determine volume: %s" % vol)
            else:
                raise TypeError("Volume unsupported type: %s" % type(vol))

            cvolume.values[i] = self._clamp(cvolume.values[i], base)

    def _clamp(self, vol, base):
        if vol / base > self._max_vol:
            return int(base * self._max_vol)
        else:
            return vol

    def get_sink_mute(self, sink: str = None):
        """Returns if the given sink, or the default sink if not specificed, is
        muted.
        """
        sink = self._default_sink if sink == None else sink.encode()

        pa_threaded_mainloop_lock(self._mainloop)

        self._get_sink_info(sink)

        mute = self._sink_info.contents.mute

        pa_threaded_mainloop_accept(self._mainloop)
        pa_threaded_mainloop_unlock(self._mainloop)

        return bool(mute)

    def get_sink_volume(self, sink: str = None):
        """Returns the volume of the given sink, or the default sink if not
        specified.
        """
        sink = self._default_sink if sink == None else sink.encode()

        pa_threaded_mainloop_lock(self._mainloop)

        self._get_sink_info(sink)

        channels = int(self._sink_info.contents.volume.channels)
        values = list(self._sink_info.contents.volume.values)[:channels]
        base_volume = self._sink_info.contents.base_volume

        pa_threaded_mainloop_accept(self._mainloop)
        pa_threaded_mainloop_unlock(self._mainloop)

        for i, value in enumerate(values):
            values[i] = value / base_volume

        return values

    def get_sink_info(self, sink: str = None):
        """Return the sink info of the given sink, or the default sink if not
        specified.
        """
        sink = self._default_sink if sink == None else sink.encode()

        pa_threaded_mainloop_lock(self._mainloop)

        self._get_sink_info(sink)

        sink_info = SinkInfo.from_pa_sink_info(self._sink_info.contents)

        pa_threaded_mainloop_accept(self._mainloop)
        pa_threaded_mainloop_unlock(self._mainloop)

        return sink_info

    def get_server_info(self):
        """Returns information about the connected server."""
        pa_threaded_mainloop_lock(self._mainloop)

        self._get_server_info()

        server_info = ServerInfo.from_pa_server_info(self._server_info.contents)

        pa_threaded_mainloop_accept(self._mainloop)
        pa_threaded_mainloop_unlock(self._mainloop)

        return server_info

    def subscribe(self, cb):
        self._subscribe_cbs.append(cb)
        return cb
