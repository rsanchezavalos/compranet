import subprocess
import os
import luigi
from luigi import configuration
from utils.pg_compranet import parse_cfg_string

class historico_funcionarios(luigi.WrapperTask):
    """
    """

    def requires(self):
        nombres_funcionarios = #pendiente: leer la lista en un formato con sentido
        for nombre in nombres_funcionarios:
            yield parse_cv(nombre_funcionario = nombre) 
            #pendiente: esto está feo
            #pendiente: ¿cómo pasarle fechas a esto?
        


class parse_cv(luigi.Task):
    """
    """

    nombre_funcionario = luigi.Parameter()

    def requires(self):
        yield crawl_funcionario(nombre_funcionario)

    def run(self):
    #pendiente

    def output(self):
    #pendiente: 


class crawl_funcionario(luigi.Task):
    """
    """

    nombre_funcionario = luigi.Parameter()

    def requires(self):
        yield lista_funcionarios()

    def run(self):
        # pendiente: pasarle a declaranet.py el nombre de funcionario

    def output(self):
        #pendiente: path a s3://funcionarios



class ingesta_datos(luigi.WrapperTask):
    """
    Task principal de ingesta
    """
    root_ingest_path = luigi.Parameter()

    def requires(self):
        yield ingesta_funcionarios()
        yield ingesta_contribuyentes()
        yield ingesta_compranet()
        yield ingesta_UCs()
        yield ingesta_claves_sal()


class ingesta_funcionarios(luigi.Task):
    """
    """

    def requires(self):
        yield descarga_funcionarios()

    def run(self):
        # pendiente: subir a s3

    def output(self):
        output_path = '' #pendiente: path a s3
        return luigi.s3.S3Target(path=output_path)


class ingesta_contribuyentes(luigi.Task):
    """
    """

    def requires(self):
        yield descarga_contribuyentes()

    def run(self):
        # pendiente subir a s3

    def output(self):
        output_path = '' #pendiente: path a s3
        return luigi.s3.S3Target(path=output_path)


class ingesta_compranet(luigi.Task):
    """
    """

    def requires(self):
        yield descarga_compranet()

    def run(self):
        # pendiente: subir a s3

    def output(self):
        output_path = '' #pendiente: path a s3
        return luigi.s3.S3Target(path=output_path)

class ingesta_UCs(luigi.Task):
    """
    """

    def requires(self):
        yield descarga_UCs()

    def run(self):
        # pendiente: subir a s3

    def output(self):
        output_path = '' #pendiente: path a s3
        return luigi.s3.S3Target(path=output_path)

class ingesta_claves_sal(luigi.Task): 
    """
    """

    def requires(self):
        yield descarga_claves_sal()

    def run(self):
        # pendiente: subir a s3

    def output(self):
        output_path = '' #pendiente: path a s3
        return luigi.s3.S3Target(path=output_path)  


class descarga_funcionarios(luigi.Task):
    """
    """

    def requires(self):
        pass

    def run(self):
        conf = configuration.get_config()
        bash_path = parse_cfg_string(conf.get("DEFAULT", "bash_path"))
        
        cmd = '''
            {}/funcionarios.sh
        '''.format(bash_path)

        subprocess.call(cmd, shell=True)
        return

    def output(self):
        return luigi.LocalTarget(str(self.root_ingest_path) + "/funcionarios.csv")


class descarga_contribuyentes(luigi.Task):
    """
    """

    def requires(self):
        pass

    def run(self):
        conf = configuration.get_config()
        bash_path = parse_cfg_string(conf.get("DEFAULT", "bash_path"))
        
        cmd = '''
            {}/contribuyentes.sh
        '''.format(bash_path)

        subprocess.call(cmd, shell=True)

        return

    def output(self):
        return luigi.LocalTarget(str(self.root_ingest_path) + "/contribuyentes.csv")


class descarga_compranet(luigi.Task):
    """
    """

    def requires(self):
        pass

     def run(self):
        conf = configuration.get_config()
        bash_path = parse_cfg_string(conf.get("DEFAULT", "bash_path"))
        
        cmd = '''
            {}/compranet.sh
        '''.format(bash_path)

        subprocess.call(cmd, shell=True)

        return


    def output(self):
        return luigi.LocalTarget(str(self.root_ingest_path) + "/compranet.csv")


class descarga_UCs(luigi.Task):
    """
    """

    def requires(self):
        pass

    def run(self):
        conf = configuration.get_config()
        bash_path = parse_cfg_string(conf.get("DEFAULT", "bash_path"))
        
        cmd = '''
            {}/unidades_compradoras.sh
        '''.format(bash_path)

        subprocess.call(cmd, shell=True)

        return

    def output(self):
        return luigi.LocalTarget(str(self.root_ingest_path) + "/unidades_compradoras.csv")


class descarga_claves_sal(luigi.Task):
    """
    """

    def requires(self):
        pass

    def run(self):
        conf = configuration.get_config()
        bash_path = parse_cfg_string(conf.get("DEFAULT", "bash_path"))
        
        cmd = '''
            {}/claves_salariales.sh
        '''.format(bash_path)

        subprocess.call(cmd, shell=True)

    def output(self):
        return luigi.LocalTarget(str(self.root_ingest_path) + "/claves_salariales.sh")