.. _introduction-overview:

########
Overview
########

Scripture Burrito is a data interchange format for Bible-centric content, designed to make Scripture translation projects portable between tools, platforms, and archiving systems.

A translation project typically contains dozens or hundreds of files. Without a manifest, those files are bewildering — software has no starting point for understanding what each file contains, what role it plays, or how the pieces fit together. Scripture Burrito provides that manifest. It describes all the files in a project: what each file contains, what format it is in, what part of Scripture it covers, and what role it plays. The manifest is independent of how the files are stored or distributed — they may be in a zip file, a directory, a GitHub repository, a database, or delivered via API. That manifest, together with the files it describes, is called a *burrito*. The files themselves are called *ingredients*.

Burritos are organized by *flavor*, which describes what kind of content the project contains. Currently defined flavors are Scripture Text and Scripture Audio. A *reference system* describes how content is navigated — typically by book, chapter, and verse.

Concepts
========

.. include:: /includes/burrito.txt

.. include:: /includes/flavor_types.txt

.. include:: /includes/flavors.txt

.. include:: /includes/reference_system.txt

.. include:: /includes/ingredients.txt


Goals
=====

#. Scripture Burrito is designed for **data interchange** between ecosystems and as a **portable archive format** for translation projects, covering all tools in the translation and publication process from initial drafting through checking, publication, and revision.

#. Non-text formats such as audio and sign language are **first-class content**, not add-ons to a text translation.

#. A burrito exported from one tool can be imported into another and back without data loss.

Acknowledgements
================

Scripture Burrito was developed through a multi-year collaboration between `American Bible Society <https://americanbible.org/>`_, `Biblica <https://www.biblica.com/>`_, `Bridge Connectivity Solutions <https://bridgeconn.com/>`_, `Clear.Bible <https://www.clear.bible/>`_, `Eldarion <https://eldarion.com/>`_, `SIL <https://www.sil.org/>`_, `Seed Company <https://seedcompany.com/>`_, `unfoldingWord <https://www.unfoldingword.org/>`_, and `United Bible Societies <https://unitedbiblesocieties.org/>`_, with sponsorship from `illumiNations <https://illuminations.bible/>`_.
