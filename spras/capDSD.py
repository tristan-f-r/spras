from pathlib import Path

from spras.containers import prepare_volume, run_container_and_log
from spras.dataset import Dataset
from spras.interactome import convert_undirected_to_directed
from spras.prm import PRM

__all__ = ['CapDSD']

class CapDSD(PRM):
    required_inputs = ['ppi']

    @staticmethod
    def generate_inputs(data: Dataset, filename_map: dict[str, str]):
        """
        Access fields from the dataset and write the required input files
        @param data: dataset
        @param filename_map: a dict mapping file types in the required_inputs to the filename for that type
        """
        for input_type in CapDSD.required_inputs:
            if input_type not in filename_map:
                raise ValueError(f"{input_type} filename is missing")

        # create the ppi
        ppi = data.get_interactome()
        ppi = convert_undirected_to_directed(ppi)
        ppi.to_csv(filename_map['ppi'], sep='\t', index=False, columns=["Interactor1", "Interactor2", "Weight"],
                   header=False)

    @staticmethod
    def run(ppi=None, ppip=None, output_file=None, container_framework="docker"):
        """
        Run BTB with Docker
        @param ppi:  input interactome file containing only undirected edges (required)
        @param ppip:  input interactome file containing only directed edges (required)
        @param output_file: path to the output matrix (required)
        @param container_framework: specify a container framework
        """
        if not ppi or not output_file:
            raise ValueError("Required capDSD arguments are missing")

        work_dir = '/capDSD'

        volumes = list()

        bind_path, ppi_file = prepare_volume(ppi, work_dir)
        volumes.append(bind_path)

        # Create a prefix for the output filename and ensure the directory exists
        out_dir = Path(output_file).parent
        out_dir.mkdir(parents=True, exist_ok=True)
        bind_path, mapped_out_dir = prepare_volume(str(out_dir), work_dir)
        volumes.append(bind_path)
        mapped_out_prefix = mapped_out_dir + '/output'

        container_suffix = "capdsd"

        # Since the volumes are binded under different folders, we can safely
        # use the ppip_file's parent.
        command = ['python',
                   '/capDSD/DSD.py',
                   '-c',
                   ppi_file, mapped_out_prefix]


        run_container_and_log('capDSD',
                              container_framework,
                              container_suffix,
                              command,
                              volumes,
                              work_dir)

        output_matrix = Path(out_dir) / 'output.dsd'
        output_matrix.rename(output_file)

        # We postprocess the DSD output with the weighed
        # majority voting algorithm proposed in
        # https://doi.org/10.1371/annotation/343bf260-f6ff-48a2-93b2-3cc79af518a9

    @staticmethod
    def parse_output(raw_pathway_file: str, standardized_pathway_file: str):
        pass
