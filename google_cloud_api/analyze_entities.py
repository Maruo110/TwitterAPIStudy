# -*- coding: utf-8 -*-

def getAnalizeEntityResult(text_content):
    from google.cloud import language_v1
    from google.cloud.language_v1 import enums

    client = language_v1.LanguageServiceClient()

    type_ = enums.Document.Type.PLAIN_TEXT

    language = "ja"
    document = {"content": text_content, "type": type_, "language": language}

    encoding_type = enums.EncodingType.UTF8

    response = client.analyze_entities(document, encoding_type=encoding_type)
    return response

"""
    # Loop through entitites returned from the API
    for entity in response.entities:
        print(u"Representative name for the entity: {}".format(entity.name))
        print(u"Entity type: {}".format(enums.Entity.Type(entity.type).name))
        print(u"Salience score: {}".format(entity.salience))

        for metadata_name, metadata_value in entity.metadata.items():
            print(u"{}: {}".format(metadata_name, metadata_value))

        for mention in entity.mentions:
            print(u"Mention text: {}".format(mention.text.content))
            print(u"Mention type: {}".format(enums.EntityMention.Type(mention.type).name))

"""