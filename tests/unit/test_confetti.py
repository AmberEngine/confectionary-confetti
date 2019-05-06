from confetti import Confetti


def test_confetti():
    path = "/Path/To/Parameters"
    confetti = Confetti(confetti_path=path)

    assert confetti.path == path
