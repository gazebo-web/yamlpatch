# Ignition YAMLPatch

# YAML Patch is a yamlpath wrapper that allows patching yaml config files

from types import SimpleNamespace
from argparse import Namespace

from yamlpath import Processor, YAMLPath
from yamlpath.common import Parsers
from yamlpath.wrappers import ConsolePrinter
from yamlpath.exceptions import YAMLPathException
from yamlpath.merger.exceptions import MergeException
from yamlpath.merger import Merger, MergerConfig
from urllib.request import urlopen
from urllib.parse import urlparse


def setup_logger():
    """
    Set up a logger that prints information into the terminal.
    :return: A console printer instance.
    """
    args = SimpleNamespace(quiet=False, verbose=True, debug=False)
    return ConsolePrinter(args)


def setup_editor():
    """
    Set up a YAML editor that is capable of parsing yaml files.
    :return: A YAML editor.
    """
    return Parsers.get_yaml_editor()


def setup_merger(log, base):
    """
    Set up a merger that enables merging different patches with a base file.
    :param log: The logger instance used to print errors.
    :param base: The parsed base file that will be used during when applying the different patches.
    :return: A merger instance.
    """
    args = Namespace()
    return Merger(log, base, MergerConfig(log, args))


def setup_processor(log, data):
    """
    Set up a processor that allows reading yaml files (used for reading the yamlpatcher.yaml file)
    :param log: The logger instance used to print errors.
    :param data: The content of a file.
    :return: A Processor instance.
    """
    return Processor(log, data)


def load_file(editor, filepath):
    """
    Loads a file located in the given filepath.
    :param editor: An editor initialized by setup_editor.
    :param filepath: The path of the file that needs to be opened.
    :return: The file content or an exception if the file does not exist.
    """
    (data, ok) = Parsers.get_yaml_data(editor, log, filepath)
    if not ok:
        raise FileNotFoundError("File does not exist: " + filepath)
    return data


def write_output(editor, filepath, data):
    """
    Writes data into a file that will be located in the given filepath.
    :param editor: An editor initialized by setup_editor.
    :param filepath: The path of the file that needs to be opened.
    :param data: The content of a file.
    """
    file = open(filepath, 'w')
    editor.dump(data, file)
    file.close()


def load_base_filepath(config):
    """
    Reads the `base` field from the yamlpatcher.yaml file and returns its value.
    :param config: The content of the config file.
    :return: The base filepath gotten from the base field.
    """
    fp = "base.yaml"
    nodes = config.get_nodes(YAMLPath("base"), mustexist=True)
    for n in nodes:
        fp = str(n)
    return fp


def load_patch_filepaths(config):
    """
    Reads the `patches` field from the yamlpatcher.yaml file and returns its value.
    :param config: The content of the config file.
    :return: An array with the different patches file paths.
    """
    fps = []
    nodes = config.get_nodes(YAMLPath("patches"), mustexist=False)
    for n in nodes:
        fps = n.node
    return fps


def load_output_filepath(config):
    """
    Reads the `output` field from the yamlpatcher.yaml file and returns its value.
    :param config: The content of the config file.
    :return: The output filepath gotten from the output field.
    """
    fp = "output.yaml"
    nodes = config.get_nodes(YAMLPath("output"), mustexist=True)
    for n in nodes:
        fp = str(n)
    return fp


if __name__ == '__main__':
    log = setup_logger()
    editor = setup_editor()

    try:
        log.info("Reading yamlpatcher.yaml config file")
        configFile = load_file(editor, "yamlpatcher.yaml")
        config = setup_processor(log, configFile)

        filepathBase = load_base_filepath(config)
        filepathPatches = load_patch_filepaths(config)
        filepathOutput = load_output_filepath(config)

        base = load_file(editor, filepathBase)

        merger = setup_merger(log, base)

        for filepathPatch in filepathPatches:
            log.info("Merging with {}".format(filepathPatch))
            patch = load_file(editor, filepathPatch)
            merger.merge_with(patch)

        log.info("Writing output: {}".format(filepathOutput))
        merger.prepare_for_dump(editor, filepathOutput)
        write_output(editor, filepathOutput, merger.data)

        log.info("YAML-Patch successfully finished patching {} into {} file".format(filepathBase, filepathOutput))

    except FileNotFoundError as ex:
        log.debug(ex)
        exit(1)
    except MergeException as ex:
        log.debug(ex)
        exit(2)
    except YAMLPathException as yex:
        log.debug(yex)
        exit(3)
