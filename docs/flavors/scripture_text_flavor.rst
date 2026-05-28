.. _scripture_text_flavor:

##############
Scripture Text
##############

======
Status
======

The **Scripture Text** flavor represents the textual content of a Scripture translation or original-language edition.  
It corresponds to Paratext’s project format and the Digital Bible Library (DBL) “text entry” type.

This flavor is designed for any collection of Scripture books in **USFM**, **USX**, or **USJ** format, together with the supporting metadata and language resources needed to make the text portable, verifiable, and self-describing.

A typical Scripture Text burrito originates from a Paratext export, which includes:

* A ``metadata.json`` file describing the project
* One text file per canonical book (``.SFM``, ``.USFM``, ``.USX``, or ``.USJ``)
* A ``versification.json`` file defining the verse system
* One or more ``.ldml`` locale files
* Optional supporting files (fonts, stylesheets, license, etc.)

As of 2025, this structure aligns with the *Paratext 9.x export format* and the Scripture Burrito 1.0 schema.

=======
Content
=======

A Scripture Text burrito contains a directory of **ingredients**, each describing one textual or supporting resource.  
Each ingredient lists its checksum, size, MIME type, and role within the project.

Typical ingredient types include:

--------------------
Textual Ingredients
--------------------

Scripture Text supports three serializations of the same underlying format:

* **USFM** is familiar to Bible translators and is recommended for translations in progress.
* **USX** (the XML expression of USFM) contains machine-readable reference information that cannot be represented in USFM. Valid USFM can be round-tripped to USX; USX cannot be round-tripped to USFM without losing those references. USX is recommended for valid content oriented toward publication.
* **USJ** is the JSON serialization of USFM, useful for programmatic processing.

* ``*.SFM`` / ``*.USFM`` — Standard Paratext markup files (one per canonical book)
  * **mimeType:** ``text/x-usfm``
  * **scope:** Lists book code(s) (e.g. ``"scope": {"MAT": []}``)
  * **naming convention:** Paratext numeric prefix + three-letter book code

* ``*.USX`` — XML serialization of USFM
  * **mimeType:** ``application/xml``
  * **scope:** Lists book code(s)
  * **role:** ``text``

* ``*.USJ`` — JSON serialization of USFM
  * **mimeType:** ``application/json``
  * **scope:** Lists book code(s)
  * **role:** ``text``

* ``versification.json`` — Defines the verse mapping used in this translation  
  * **mimeType:** ``application/json``  
  * **role:** ``versification``  
  * **format:** Follows the *Copenhagen Alliance Versification* standard, which specifies canonical book order, chapter and verse structure, and mappings between versification systems.

---------------------
Language and Settings
---------------------

* ``*.ldml`` — Locale Data Markup Language file defining language and script settings  
  * **mimeType:** ``application/xml``  
  * **role:** ``localedata``

-------------------
Optional Resources
-------------------

* ``styles.xml`` — Style definitions for rendering (optional)
* ``license.json`` — License or permissions statement (optional)
* ``custom.sty`` — Paratext custom style sheet (optional)
* Fonts or auxiliary metadata files as needed

-----------
Example
-----------

From the Paratext export *EZPEZ Clone*:

::

   ingredients/
       01GENEIEIO.SFM
       41MATEIEIO.SFM
       45ACTEIEIO.SFM
       67REVEIEIO.SFM
       en.ldml
       versification.json

Each book file contains one canonical book in USFM format. The ``versification.json`` defines the reference scheme (following the Copenhagen Alliance format). The ``.ldml`` file defines locale data such as collation and numeric formatting.

=======================
Metadata Flavor Details
=======================

-----------
projectType
-----------

Indicates the project’s relationship to other projects. One of:

* ``standard`` — A normal translation or edition  
* ``daughter`` — Derived from a parent translation  
* ``studyBible`` — A full study Bible project  
* ``studyBibleAdditions`` — Commentary or helps supplementing a study Bible  
* ``backTranslation`` — A reverse translation for checking purposes  
* ``auxiliary`` — Supplemental or experimental project  
* ``transliterationManual`` — Manual transliteration of text  
* ``transliterationWithEncoder`` — Automatically generated transliteration

---------------
translationType
---------------

Describes the translation’s stage or intent. One of:

* ``firstTranslation`` — First-time translation into a language  
* ``newTranslation`` — A new translation independent of existing versions  
* ``revision`` — A revision of a prior translation  
* ``studyOrHelpMaterial`` — Study notes or supplementary helps

--------
audience
--------

Describes the intended readership. One of:

* ``basic`` — Simplified or learner audience  
* ``common`` — General-purpose translation  
* ``commonLiterary`` — Common audience with elevated literary style  
* ``literary`` — Formal, literary audience  
* ``liturgical`` — Designed for public worship  
* ``children`` — Adapted for young readers

-----------
usfmVersion
-----------

Specifies the schema version of USFM or USX used.  
For Paratext 9 exports, typical values include:

* ``2.6.0`` — USFM 2.6  
* ``3.0.0`` — USFM 3.0 or later  
* ``3.1.0`` — Current USFM schema version as of 2025

===========
Conventions
===========

-------
textFiles
-------

Each canonical book is stored as one text file (``.SFM``, ``.USFM``, ``.USX``, or ``.USJ``), named using the **Paratext numeric prefix** and **book code** convention:

* ``41MATEIEIO.SFM`` → Gospel of Matthew  
* ``45ACTEIEIO.SFM`` → Acts of the Apostles  
* ``67REVEIEIO.SFM`` → Revelation  

This convention ensures stable ordering and identification across tools.

-------
versification
-------

Every Scripture Text burrito must include a ``versification.json`` file.  
This file conforms to the **Copenhagen Alliance Versification** format, which provides a canonical list of books, chapters, and verses, along with optional mappings to standard versification systems (e.g. English, Hebrew, Vulgate).

-------------------
localeInformation
-------------------

Each ``.ldml`` file contains language- and script-level data, such as:

* Collation order  
* Number and date formats  
* Script direction (``ltr`` or ``rtl``)  
* Language tag (BCP-47)

Multiple LDML files may be included for multilingual projects.

-----------------
localizedNames
-----------------

The ``localizedNames`` section maps Paratext book codes (e.g. ``MAT``, ``ROM``, ``1CO``) to localized display names in one or more languages.  
Example:

::

   "MAT": {
     "short": {"en": "Matthew"},
     "long": {"en": "The Gospel according to Matthew"}
   }

-------------------------
typesetAsVersedParagraphs
-------------------------

A consumer hint for presentation. When this flag is present, each verse or verse range should be displayed as a separate paragraph, regardless of paragraph markers in the USFM. When absent, consumers should respect paragraph markers as encoded.

===================
Schema Conformance
===================

A valid Scripture Text burrito **must include**:

+--------------------------+------------------------------------------------+
| **Field**                | **Description**                                |
+--------------------------+------------------------------------------------+
| ``meta``                 | Source info and generation metadata            |
| ``type.flavorType.name`` | ``"scripture"``                                |
| ``type.flavorType.flavor`` | Must specify name, projectType, etc.        |
| ``languages``            | One or more with BCP-47 tag and script         |
| ``ingredients``          | Book files, versification, and locale data     |
| ``versification.json``   | Copenhagen Alliance Versification definition   |
+--------------------------+------------------------------------------------+

Optional fields:

* ``localizedNames`` — Recommended for user-facing tools  
* ``license.json`` — Encouraged for public sharing  
* ``custom.sty`` or ``styles.xml`` — Optional for rendering

====================
Illustrative Example
====================

::

   {
     "type": {
       "flavorType": {
         "name": "scripture",
         "flavor": {
           "name": "textTranslation",
           "projectType": "standard",
           "translationType": "firstTranslation",
           "audience": "common",
           "usfmVersion": "2.6.0"
         }
       }
     },
     "languages": [
       {
         "tag": "en",
         "name": {"en": "English (eng)"},
         "scriptDirection": "ltr"
       }
     ],
     "ingredients": {
       "ingredients/41MATEIEIO.SFM": {
         "size": 160897,
         "mimeType": "text/x-usfm",
         "scope": {"MAT": []}
       },
       "ingredients/versification.json": {
         "size": 27334,
         "mimeType": "application/json",
         "role": "versification"
       },
       "ingredients/en.ldml": {
         "size": 3492,
         "mimeType": "application/xml",
         "role": "localedata"
       }
     }
   }

This structure corresponds to a typical Paratext-generated *Scripture Text* burrito, supporting USFM, USX, or USJ formats, and conforming fully to the Scripture Burrito schema.

