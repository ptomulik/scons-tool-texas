USER MANUAL
-----------

This directory (``doc/user``) contains user manual for TeXAS tool. Entire
source for user manual is contained in ``manual.xml``.


EDITING SOURCE
^^^^^^^^^^^^^^

I use jEdit_ when necessary. Normally edit with vim + `vim xml plugin`_.

Note, I have tried Eclipse_ with Vex_ plugin but it deletes comments and
``<!DOCTYPE...>`` tag where I declare local entities. It also messes up with
attributes, for example it uses ``id`` instead of ``xml:id``. Other free
editors do not support DocBook 5 or do not support RELAX NG schemas.

VALIDATING
^^^^^^^^^^

You may use jing_ RELAX NG validator to validate the ``manual.xml``::

    jing http://docbook.org/xml/5.0/rng/docbook.rng manual.xml

You may also validate with xmllint, which is a part of libxml_ package::

    xmllint --noout --relaxng http://docbook.org/xml/5.0/rng/docbook.rng manual.xml

BUILDING
^^^^^^^^

To build user manual type::
  
    scons -u user-doc

Resulting document will be written to files under ``#build/doc/user/``.

.. _jEdit: http://www.jedit.org/
.. _vim xml plugin: http://www.vim.org/scripts/script.php?script_id=1397
.. _Eclipse: http://www.eclipse.org/
.. _Eclipse Marketplace Client: http://marketplace.eclipse.org/marketplace-client-intro
.. _Vex: http://www.eclipse.org/vex/
.. _jing: http://www.thaiopensource.com/relaxng/jing.html
.. _libxml: http://www.xmlsoft.org/index.html_
