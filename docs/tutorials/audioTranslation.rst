.. _tutorial-audioTranslation:

########################
Scripture Audio Tutorial
########################

[:ref:`Specification <scripture_audio_flavor>`]  [:ref:`Example <examples-audioTranslation>`]

This tutorial walks through creating a Scripture Burrito metadata file for an
audio translation project. By the end you will have a valid ``metadata.json``
that can be read by any conforming tool.

**Scenario:** The Zarma translation team (from :ref:`tutorial-textTranslation`)
has recorded an audio reading of Titus in Zarma — one MP3 file per chapter.
Each recording also has a timing file that maps verse timecodes, enabling
audio players to jump to a specific verse. We want to package these three
chapters as an audio translation burrito.

The directory looks like this::

   zarma-audio/
       media/
           dje_tit_c01.mp3
           dje_tit_c01.json
           dje_tit_c02.mp3
           dje_tit_c02.json
           dje_tit_c03.mp3
           dje_tit_c03.json

We will build the ``metadata.json`` file section by section.

=============
Common Fields
=============

*These fields are common to all burritos — see* :ref:`burrito-structure` *for the full specification.*

-------------------
1. Format and meta
-------------------

::

   {
     "format": "scripture burrito",
     "meta": {
       "version": "1.0.0",
       "category": "source",
       "generator": {
         "softwareName": "Orature",
         "softwareVersion": "2.0.0",
         "userName": "Fatima Maïga"
       },
       "defaultLocale": "dje",
       "dateCreated": "2025-11-10T14:00:00+01:00"
     },

--------------------------
2. Identification section
--------------------------

::

     "identification": {
       "name": {
         "en": "Zarma NT Audio — Titus",
         "dje": "Zarma Neeriya Koyra — Tit"
       },
       "abbreviation": {
         "en": "ZJNT-audio"
       }
     },

--------------------
3. Languages section
--------------------

::

     "languages": [
       {
         "tag": "dje",
         "name": {
           "en": "Zarma",
           "dje": "Zarmaciine"
         }
       }
     ],

-------------------
4. Agencies section
-------------------

::

     "agencies": [
       {
         "id": "https://seedcompany.com",
         "roles": ["rightsHolder", "content"],
         "url": "https://seedcompany.com",
         "name": {"en": "Seed Company"},
         "abbr": {"en": "SC"}
       }
     ],

---------------------
5. Common Ingredients
---------------------

The ``ingredients`` object maps every file path (relative to the burrito root)
to a descriptor. These fields appear in every burrito regardless of flavor:

* **file path** (the key) — relative to the burrito root, using forward
  slashes. Must match the actual layout exactly.
* **checksum** — used by receiving tools to verify file integrity. MD5 is
  currently the standard algorithm.
* **mimeType** — identifies the file format. Allowed values are
  flavor-specific; see below.
* **size** — file size in bytes.
* **scope** — lists the chapters the file contains. Each book code maps to a
  list of chapter strings (or an empty array for all chapters).
* **role** — for support files that are not primary audio. Allowed values are
  flavor-specific; see below.

=======================
Scripture Audio Fields
=======================

*These fields are specific to the Scripture Audio flavor — see*
:ref:`scripture_audio_flavor` *for the full specification.*

---------------
6. Type section
---------------

For an audio translation the ``flavorType.name`` is ``"scripture"`` and the
``flavor.name`` is ``"audioTranslation"``::

     "type": {
       "flavorType": {
         "name": "scripture",
         "flavor": {
           "name": "audioTranslation",
           "performance": ["singleVoice", "reading"],
           "formats": {
             "format-mp3": {
               "compression": "mp3",
               "trackConfiguration": "1/0 (Mono)",
               "bitRate": 128000,
               "samplingRate": 44100
             }
           }
         },
         "currentScope": {
           "TIT": ["1", "2", "3"]
         }
       }
     },

* ``performance`` must include one voice type (``"singleVoice"`` or
  ``"multipleVoice"``) and one delivery style (``"reading"`` or ``"drama"``).
  Optional values include ``"withMusic"``, ``"withEffects"``,
  ``"withHeadings"``.
* ``formats`` describes the technical properties of the audio files. The key
  (``"format-mp3"``) is an arbitrary label; the value records the compression,
  track configuration, and encoding parameters.
* ``currentScope`` lists the chapters present. Chapter numbers are strings.
  An empty array (``[]``) means all chapters of the book are included.

------------------------------
7. Flavor-Specific Ingredients
------------------------------

Audio files must use one of these MIME types:

* ``"audio/mpeg"`` for MP3 files
* ``"audio/ogg;codecs=opus"`` for OGG Opus files
* ``"audio/wav"`` for WAV files

The ``scope`` for audio files uses chapter strings matching ``currentScope``.
For verse-range recordings use strings like ``"1:1-21"`` instead of chapter
numbers.

Support file role defined for this flavor:

* ``"timing"`` — a JSON file mapping verse timecodes for a paired audio file.
  Timing files carry the same ``scope`` as their audio file.

The full ``ingredients`` object for the Zarma Titus audio::

     "ingredients": {
       "media/dje_tit_c01.mp3": {
         "checksum": {"md5": "f9bcf3872446a7d50e66c24d5692f7c7"},
         "mimeType": "audio/mpeg",
         "size": 1165070,
         "scope": {"TIT": ["1"]}
       },
       "media/dje_tit_c01.json": {
         "checksum": {"md5": "bc6e1fa1109126fb6b14e4f41bbde378"},
         "mimeType": "application/json",
         "size": 1596,
         "scope": {"TIT": ["1"]},
         "role": "timing"
       },
       "media/dje_tit_c02.mp3": {
         "checksum": {"md5": "9ee007594822f19e8e1ce6ab5d788004"},
         "mimeType": "audio/mpeg",
         "size": 933938,
         "scope": {"TIT": ["2"]}
       },
       "media/dje_tit_c02.json": {
         "checksum": {"md5": "eb5f27a17956220b848d19f0b9b6720b"},
         "mimeType": "application/json",
         "size": 1445,
         "scope": {"TIT": ["2"]},
         "role": "timing"
       },
       "media/dje_tit_c03.mp3": {
         "checksum": {"md5": "a7a8ce6c238dc260c349e12d89efbdaf"},
         "mimeType": "audio/mpeg",
         "size": 1038010,
         "scope": {"TIT": ["3"]}
       },
       "media/dje_tit_c03.json": {
         "checksum": {"md5": "3450197390f0351547be11047ba68b5e"},
         "mimeType": "application/json",
         "size": 1445,
         "scope": {"TIT": ["3"]},
         "role": "timing"
       }
     }

=================
The complete file
=================

::

   {
     "format": "scripture burrito",
     "meta": {
       "version": "1.0.0",
       "category": "source",
       "generator": {
         "softwareName": "Orature",
         "softwareVersion": "2.0.0",
         "userName": "Fatima Maïga"
       },
       "defaultLocale": "dje",
       "dateCreated": "2025-11-10T14:00:00+01:00"
     },
     "identification": {
       "name": {
         "en": "Zarma NT Audio — Titus",
         "dje": "Zarma Neeriya Koyra — Tit"
       },
       "abbreviation": {
         "en": "ZJNT-audio"
       }
     },
     "languages": [
       {
         "tag": "dje",
         "name": {
           "en": "Zarma",
           "dje": "Zarmaciine"
         }
       }
     ],
     "type": {
       "flavorType": {
         "name": "scripture",
         "flavor": {
           "name": "audioTranslation",
           "performance": ["singleVoice", "reading"],
           "formats": {
             "format-mp3": {
               "compression": "mp3",
               "trackConfiguration": "1/0 (Mono)",
               "bitRate": 128000,
               "samplingRate": 44100
             }
           }
         },
         "currentScope": {
           "TIT": ["1", "2", "3"]
         }
       }
     },
     "agencies": [
       {
         "id": "https://seedcompany.com",
         "roles": ["rightsHolder", "content"],
         "url": "https://seedcompany.com",
         "name": {"en": "Seed Company"},
         "abbr": {"en": "SC"}
       }
     ],
     "ingredients": {
       "media/dje_tit_c01.mp3": {
         "checksum": {"md5": "f9bcf3872446a7d50e66c24d5692f7c7"},
         "mimeType": "audio/mpeg",
         "size": 1165070,
         "scope": {"TIT": ["1"]}
       },
       "media/dje_tit_c01.json": {
         "checksum": {"md5": "bc6e1fa1109126fb6b14e4f41bbde378"},
         "mimeType": "application/json",
         "size": 1596,
         "scope": {"TIT": ["1"]},
         "role": "timing"
       },
       "media/dje_tit_c02.mp3": {
         "checksum": {"md5": "9ee007594822f19e8e1ce6ab5d788004"},
         "mimeType": "audio/mpeg",
         "size": 933938,
         "scope": {"TIT": ["2"]}
       },
       "media/dje_tit_c02.json": {
         "checksum": {"md5": "eb5f27a17956220b848d19f0b9b6720b"},
         "mimeType": "application/json",
         "size": 1445,
         "scope": {"TIT": ["2"]},
         "role": "timing"
       },
       "media/dje_tit_c03.mp3": {
         "checksum": {"md5": "a7a8ce6c238dc260c349e12d89efbdaf"},
         "mimeType": "audio/mpeg",
         "size": 1038010,
         "scope": {"TIT": ["3"]}
       },
       "media/dje_tit_c03.json": {
         "checksum": {"md5": "3450197390f0351547be11047ba68b5e"},
         "mimeType": "application/json",
         "size": 1445,
         "scope": {"TIT": ["3"]},
         "role": "timing"
       }
     },
     "copyright": {
       "shortStatements": [
         {
           "statement": "CC BY-SA 4.0",
           "mimetype": "text/plain",
           "lang": "en"
         }
       ]
     }
   }

==========
Next steps
==========

* To cover verse ranges instead of whole chapters, use scope strings like
  ``"1:1-21"`` and update ``currentScope`` accordingly.
* To package audio in multiple formats (MP3 and WAV), add entries in both
  ``formats`` and ``ingredients`` — both files can share the same scope.
* For the timing file format, see :ref:`tutorial-audioAlignment`.
* For the complete field reference see :ref:`scripture_audio_flavor`.
