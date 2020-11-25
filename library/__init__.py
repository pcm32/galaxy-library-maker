import os
import yaml
import logging
import bioblend.galaxy

class Library(object):
    """
    Loads libraries encoded in YAML like:

    - library: <name-of-library>
      desc: <description>
      synopsis: <synopsis>
      base_dir: <path>
      recursive: true
      extensions:
         - rdata: <galaxy-datatype>
         - ad: 'h5ad'
    - library: 'second_library'
      recursive: false
      base_dir: /some/path/to/files
      extensions:
         - mtx: '10x_mtx_galaxy_datatype'

    """

    def __init__(self, title, desc, synopsis, base_dir, extensions, recursive=True):
        self.name = title
        self.desc = desc
        self.synopsis = synopsis
        self.base_dir = base_dir
        self.files = {}
        self.galaxy_lib = None

        for dirpath, dirs, files in os.walk(base_dir):
            for f in files:
                filename, file_extension = os.path.splitext(f)
                if file_extension in extensions:
                    files[os.path.join(dirpath, f)] = extensions[file_extension]
                if not recursive:
                    return

    @staticmethod
    def read_from_yaml(path_yaml):
        """
        Produces a list of Libraries read from the file system, ready to be checked against Galaxy for loading.

        :param path_yaml: path to a YAML file with the format specified in the Library class
        :return: list of Library objects, with file paths loaded.
        """

        with open(path_yaml, mode='r') as libs_def:
            libs_metadata = yaml.safe_load_all(libs_def)

        libs = list()
        for lib in libs:
            libs.append(Library(lib['library'], lib['base_dir'], lib['extensions'], bool(lib['recursive'])))

        return libs


    def absolute_path(self, relative_path):
        if relative_path in self.files:
            return os.path.join(self.base_dir, relative_path[relative_path.startswith("./") and len("./"):])
        else:
            raise ValueError(f"Relative path {relative_path} not part of library")


class LibraryGalaxyLoader(object):
    """
    Takes a list of Library objects, checks whether they are in the galaxy instance and loads them if not
    """

    def __init__(self, gi: bioblend.galaxy, lib: Library):
        """
        Initializes for a galaxy instance
        :param gi:
        """
        self.gi = gi
        self.lib = lib
        self.existing = {}

    def __check_library_availability(self, create_if_missing=True):
        glibs = self.gi.libraries.get_libraries(name=self.lib.name)
        remove = list()
        # check that we don't need to get rid of useless libraries
        for glib in glibs:
            if not glib['can_user_add']:
                logging.info(f"Ignoring library {glib['name']} as user cannot add elements to it...")
                remove.append(glib)
            elif not glib['can_user_modify']:
                logging.info(f"Ignoring library {glib['name']} as user cannot modify it...")
                remove.append(glib)
            elif glib['deleted']:
                logging.info(f"Ignoring library {glib['name']} as it is deleted...")
                remove.append(glib)
        glibs = [glib for glib in glibs if glib not in remove]
        if len(glibs) == 1:
            self.lib.galaxy_lib = glibs[0]
        elif len(glibs) > 1:
            logging.error(f"There is more than one matching library for name {self.lib.title}... please change title or delete libraries in Galaxy")
            raise ValueError
        elif create_if_missing:
            glib = self.gi.libraries.create_library(name=self.lib.name, description=self.lib.desc, synopsis=self.lib.synopsis)
            self.lib.galaxy_lib = glib

    def __check_file_availability(self, create_if_missing=True):
        if not self.lib.galaxy_lib:
            logging.error(f"Galaxy lib is not defined, call __check_library_availability() with create_if_missing to true")
        glib_id = self.lib.galaxy_lib['id']
        glib_contents = self.gi.libraries.show_library(library_id=glib_id, contents=True)
        for file_fs in self.lib.files:
            # iterate over files declared in the YAML lib
            galaxy_dataset_id, galaxy_library_folder_id, galaxy_missing_folders, galaxy_partial_folder_id = self.__find_file_in_galaxy_lib(
                file_fs, glib_contents)

            if not galaxy_dataset_id and create_if_missing:
                logging.info(f"{file_fs} not present in the library, adding it..")
                if not galaxy_library_folder_id:
                    logging.info(f"...intermediate folders not present in the library, adding them..")
                    for new_folder in galaxy_missing_folders:
                        galaxy_partial_folder_id = self.gi.libraries.create_folder(library_id=glib_id,
                                                                                   base_folder_id=galaxy_partial_folder_id,
                                                                                   folder_name=new_folder)[0]['id']
                    galaxy_library_folder_id = galaxy_partial_folder_id

                self.gi.libraries.upload_from_galaxy_filesystem(library_id=glib_id,
                                                                filesystem_paths=self.lib.absolute_path(file_fs),
                                                                folder_id=galaxy_library_folder_id,
                                                                file_type=self.lib.files[file_fs],
                                                                dbkey="?", link_data_only='link_to_files',
                                                                roles="", preserve_dirs=False, tag_using_filenames=True,
                                                                tags=None)
                # refresh glib_contents since we added files and folders.
                glib_contents = self.gi.libraries.show_library(library_id=glib_id, contents=True)
            else:
                logging.info(f"{file_fs} not present in Galaxy library, flag for creation is false, not creating it.")

    def __find_file_in_galaxy_lib(self, file_fs, glib_contents):
        path, file = os.path.split(file_fs)
        galaxy_dataset_id = None
        galaxy_library_folder_id = None
        galaxy_partial_folder_id = None
        galaxy_missing_folders = None
        for file_g in glib_contents:
            # compare to what is available in the galaxy library
            # see if we find the file and the directory, or closest directory.
            galaxy_path = "." + file_g['name']
            if galaxy_path == file_fs and file_g['type'] == 'file':
                galaxy_dataset_id = file_g['id']
            if galaxy_path == path and file_g['type'] == 'folder':
                galaxy_library_folder_id = file_g['id']
            if galaxy_path.startswith(path) and file_g['type'] == 'folder':
                missing_folders = path.replace(galaxy_path).split(os.path.sep)
                if not galaxy_partial_folder_id or len(galaxy_missing_folders) > len(missing_folders):
                    galaxy_partial_folder_id = file_g['id']
                    galaxy_missing_folders = missing_folders
        return galaxy_dataset_id, galaxy_library_folder_id, galaxy_missing_folders, galaxy_partial_folder_id


















