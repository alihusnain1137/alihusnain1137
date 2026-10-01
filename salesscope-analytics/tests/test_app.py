from pathlib import Path
from streamlit.testing.v1 import AppTest

def test_demo_and_empty_filters():
    app=AppTest.from_file(str(Path(__file__).parents[1]/'app.py')).run(timeout=30)
    assert not app.exception
    assert app.metric[2].value=='2,600'
    app.sidebar.multiselect[0].set_value([]).run()
    assert not app.exception
    assert any('No sales match' in x.value for x in app.info)

def test_upload_landing():
    app=AppTest.from_file(str(Path(__file__).parents[1]/'app.py')).run(timeout=30)
    app.sidebar.radio[0].set_value('Upload CSV').run()
    assert not app.exception
    assert any('Upload a CSV' in x.value for x in app.info)
