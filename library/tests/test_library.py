import unittest
from library import LibraryGalaxyLocator

glib_contents_1 = [
    {
     'url': '/api/libraries/f2db41e1fa331b3e/contents/Ff2db41e1fa331b3e', 'type': 'folder', 'name': '/', 'id': 'Ff2db41e1fa331b3e'
    },
    {
     'url': '/api/libraries/f2db41e1fa331b3e/contents/fa331b3eFf2db41e1', 'type': 'file', 'name': '/first_level_file', 'id': 'fa331b3eFf2db41e1'
    },
    {
     'url': '/api/libraries/f2db41e1fa331b3e/contents/Ff597429621d6eb2b', 'type': 'folder', 'name': '/nfs', 'id': 'Ff597429621d6eb2b'
    },
    {
     'url': '/api/libraries/f2db41e1fa331b3e/contents/F1cd8e2f6b131e891', 'type': 'folder', 'name': '/nfs/other_folder', 'id': 'F1cd8e2f6b131e891'
    },
    {
     'url': '/api/libraries/f2db41e1fa331b3e/contents/1cd8e2f6b131e891', 'type': 'file', 'name': '/nfs/other_folder/cellmeta', 'id': '1cd8e2f6b131e891'
    },
    {
     'url': '/api/libraries/f2db41e1fa331b3e/contents/ebfb8f50c6abde6d', 'type': 'file', 'name': '/nfs/other_folder/gtf', 'id': 'ebfb8f50c6abde6d'
    },
    {
     'url': '/api/libraries/f2db41e1fa331b3e/contents/f2db41e1fa331b3e', 'type': 'file', 'name': '/nfs/genes.txt', 'id': 'f2db41e1fa331b3e'
    },
    {
     'url': '/api/libraries/f2db41e1fa331b3e/contents/f597429621d6eb2b', 'type': 'file', 'name': '/nfs/matrix', 'id': 'f597429621d6eb2b'
    },
    {
     'url': '/api/libraries/f2db41e1fa331b3e/contents/fbebc6ab86df50de', 'type': 'file', 'name': '/nfs/other_folder/third_folder/buried_file', 'id': 'fbebc6ab86df50de'
    }
]

lgl = LibraryGalaxyLocator(glib_contents_1)

class LibraryGalaxyLocatorTest(unittest.TestCase):


    def test_find_first_level(self):
        galaxy_dataset_id, galaxy_library_folder_id, galaxy_missing_folders, galaxy_partial_folder_id = lgl.find_file('./first_level_file')
        assert galaxy_dataset_id == 'fa331b3eFf2db41e1'
        assert galaxy_library_folder_id == 'Ff2db41e1fa331b3e'
        assert len(galaxy_missing_folders) == 0

    def test_find_genes(self):
        galaxy_dataset_id, galaxy_library_folder_id, galaxy_missing_folders, galaxy_partial_folder_id = lgl.find_file(
            './nfs/genes.txt')
        assert galaxy_dataset_id == 'f2db41e1fa331b3e'
        assert galaxy_library_folder_id == 'Ff597429621d6eb2b'
        assert len(galaxy_missing_folders) == 0

    def test_first_level_missing_file(self):
        galaxy_dataset_id, galaxy_library_folder_id, galaxy_missing_folders, galaxy_partial_folder_id = lgl.find_file(
            './barcodes.txt')
        assert galaxy_dataset_id is None
        assert galaxy_partial_folder_id == 'Ff2db41e1fa331b3e'
        assert galaxy_library_folder_id == 'Ff2db41e1fa331b3e'
        assert len(galaxy_missing_folders) == 0

    def test_second_level_missing_file(self):
        galaxy_dataset_id, galaxy_library_folder_id, galaxy_missing_folders, galaxy_partial_folder_id = lgl.find_file(
            './nfs/barcodes.txt')
        assert galaxy_dataset_id is None
        assert galaxy_partial_folder_id == 'Ff597429621d6eb2b'
        assert galaxy_library_folder_id == 'Ff597429621d6eb2b'
        assert len(galaxy_missing_folders) == 0

    def test_second_level_missing_folder_file(self):
        galaxy_dataset_id, galaxy_library_folder_id, galaxy_missing_folders, galaxy_partial_folder_id = lgl.find_file(
            './nfs/store/barcodes')
        assert galaxy_dataset_id is None
        assert galaxy_partial_folder_id == 'Ff597429621d6eb2b'
        assert galaxy_library_folder_id is None
        assert len(galaxy_missing_folders) == 1
        assert 'store' in galaxy_missing_folders

    def test_third_level_file(self):
        galaxy_dataset_id, galaxy_library_folder_id, galaxy_missing_folders, galaxy_partial_folder_id = lgl.find_file(
            './nfs/other_folder/gtf')
        assert galaxy_dataset_id == 'ebfb8f50c6abde6d'
        assert galaxy_partial_folder_id == 'F1cd8e2f6b131e891'
        assert galaxy_library_folder_id == 'F1cd8e2f6b131e891'
        assert len(galaxy_missing_folders) == 0

    def test_third_level_missing_file(self):
        galaxy_dataset_id, galaxy_library_folder_id, galaxy_missing_folders, galaxy_partial_folder_id = lgl.find_file(
            './nfs/other_folder2/other_folder3/gtf')
        assert galaxy_dataset_id is None
        assert galaxy_partial_folder_id == 'Ff597429621d6eb2b'
        assert galaxy_library_folder_id is None
        assert len(galaxy_missing_folders) == 2
        assert 'other_folder3' in galaxy_missing_folders


class FileSystemLibraryTest(unittest.TestCase):
    pass
