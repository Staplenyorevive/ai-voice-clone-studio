// voice_dsp — real-time formant + pitch kernel for ai-voice-clone-studio.
// Exposes shift_formant(float32 buffer, sr, factor) to Python.
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <cmath>

namespace py = pybind11;

static py::array_t<float> shift_formant(py::array_t<float, py::array::c_style> buf, int sr, float factor) {
    auto in = buf.unchecked<1>();
    auto out = py::array_t<float>(in.shape(0));
    auto o = out.mutable_unchecked<1>();
    const float ratio = 1.0f / factor;
    for (py::ssize_t i = 0; i < in.shape(0); ++i) {
        float src = i * ratio;
        auto i0 = static_cast<py::ssize_t>(src);
        auto i1 = i0 + 1 < in.shape(0) ? i0 + 1 : i0;
        float frac = src - static_cast<float>(i0);
        o(i) = in(i0) * (1.0f - frac) + in(i1) * frac;
    }
    return out;
}

PYBIND11_MODULE(voice_dsp, m) {
    m.doc() = "voice_dsp: formant/pitch kernel for ai-voice-clone-studio";
    m.def("shift_formant", &shift_formant, "Linear-interp formant shift",
          py::arg("buf"), py::arg("sr"), py::arg("factor"));
}