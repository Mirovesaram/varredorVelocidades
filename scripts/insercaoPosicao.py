import traceback

import sys

import logging

import xml.etree.ElementTree as ET

logging.basicConfig(
    filename=r'relatorioErros.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def capturarExcecao(exctype, value, tb):

    mensagemErro="".join(traceback.format_exception(exctype,value,tb))

    print(mensagemErro)

    logging.error(mensagemErro)

if __name__ == "__main__":

    sys.excepthook = capturarExcecao

    try:

        # Carregar um arquivo .trk existente ou criar uma nova estrutura
        tree = ET.parse(r"trkCriado/2024-12-04 à(s) 18.20.47_d751cbea.trk")
        root = tree.getroot()

        # Encontrar ou criar o primeiro track existente
        track = root.find(".//track")
        if track is None:
            track = ET.SubElement(root, "track", id="1", name="Exemplo", type="pointmass", source="manual")

        # Criando o objeto PointMass com várias propriedades
        point_mass = ET.SubElement(track, "object", class_="org.opensourcephysics.cabrillo.tracker.PointMass")

        # Adicionando propriedades de massa, nome, cor, etc.
        ET.SubElement(point_mass, "property", name="mass", type="double").text = "1.0"
        ET.SubElement(point_mass, "property", name="name", type="string").text = "massa A"

        # Propriedade color com valores RGB
        color_property = ET.SubElement(point_mass, "property", name="color", type="object")
        color_object = ET.SubElement(color_property, "object", class_="java.awt.Color")
        ET.SubElement(color_object, "property", name="red", type="int").text = "255"
        ET.SubElement(color_object, "property", name="green", type="int").text = "0"
        ET.SubElement(color_object, "property", name="blue", type="int").text = "0"
        ET.SubElement(color_object, "property", name="alpha", type="int").text = "255"

        # Outras propriedades como footprint, visibility e trail
        ET.SubElement(point_mass, "property", name="footprint", type="string").text = "Footprint.Diamond"
        ET.SubElement(point_mass, "property", name="visible", type="boolean").text = "true"
        ET.SubElement(point_mass, "property", name="trail", type="boolean").text = "true"

        # Adicionando a propriedade 'framedata' com o ponto específico
        framedata_property = ET.SubElement(point_mass, "property", name="framedata", type="array", class_="[Lorg.opensourcephysics.cabrillo.tracker.PointMass$FrameData;")

        # Adicionando o quadro com as coordenadas e tempo
        frame_data_property = ET.SubElement(framedata_property, "property", name="[0]", type="object")
        frame_data_object = ET.SubElement(frame_data_property, "object", class_="org.opensourcephysics.cabrillo.tracker.PointMass$FrameData")

        # Coordenadas x, y e tempo
        ET.SubElement(frame_data_object, "property", name="x", type="double").text = "0.0004"
        ET.SubElement(frame_data_object, "property", name="y", type="double").text = "0.0008"
        ET.SubElement(frame_data_object, "property", name="time", type="double").text = "0.33"  # Tempo de exemplo

        # Salvando as alterações no arquivo
        tree.write(r"trkCriado/meuarquivo_modificado_com_objeto.trk", encoding="utf-8", xml_declaration=True)

        print("Estrutura completa adicionada ao arquivo com sucesso!")





    except Exception as e:

        capturarExcecao(*sys.exc_info())
        input("Pressione Enter para sair...")