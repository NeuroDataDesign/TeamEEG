import pyautomagic.src.Subject


def test_extract_name():
    address = 'A/B/C/name'
    expected_name = 'name'
    name = pyautomagic.src.Subject.Subject.extract_name(address)
    assert(name == expected_name)


def test_update_addresses():
    new_data_path = 'a/b/c'
    new_project_path = 'x/y/z'
    expected_data_folder = 'a/b/c/name'
    expected_project_folder = 'x/y/z/name'

    data_folder, result_folder = pyautomagic.src.Subject.Subject.update_addresses(new_data_path, new_project_path)
    assert(expected_data_folder == data_folder)
    assert(expected_project_folder == result_folder)








