# -*- coding: utf-8 -*-

#!/usr/bin/env python

# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


def run_quickstart():
    # [START language_quickstart]
    # Imports the Google Cloud client library
    # [START language_python_migration_imports]
    from google.cloud import language
    from google.cloud.language import enums
    from google.cloud.language import types
    #from google.cloud.language.types import Document
    # [END language_python_migration_imports]

    # Instantiates a client
    # [START language_python_migration_client]
    client = language.LanguageServiceClient()
    # [END language_python_migration_client]

    # The text to analyze
    text = u'新型コロナウイルスの感染拡大の影響で、アニメ業界が大きな打撃を受けている。アフレコ収録は「3密」の危険性をはらみ、アニメの素材となる作画作業も遅延。余波はタイアップ商品などにも及ぶ。'
    document = types.Document(content=text, type=enums.Document.Type.PLAIN_TEXT)

    # Detects the sentiment of the text
    sentiment = client.analyze_sentiment(document=document).document_sentiment

    print('Text: {}'.format(text))
    print('Sentiment: {}, {}'.format(sentiment.score, sentiment.magnitude))
    # [END language_quickstart]


if __name__ == '__main__':
    run_quickstart()
