.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

====================
Export Define XML ID
====================

This is a technical module needed to ease the exchange of data between multiple odoo instance.

With this module you can generate xml ids of data based on your own rules.

Or, if you define no rules on a model, it will prefix the xml id with the uid of the database.


Configuration
=============

This modules provides no user interface. Rules should be written in python code.

Inherit this module, sublcass a model and define a function '_gen_xml_id'. It should return the new xml id of the record.

.. code-block:: python

    class ProductProduct(models.Model):
        _inherit = 'product.product'
    
        def _gen_xml_id(self):
            name = '%s_%s_%s' % (
                self.company_id.name, self.barcode, self.default_code)
            return name
    

Usage
=====

Simply export some records like usual.



Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/server-tools/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed feedback.


Credits
=======

Contributors
------------

* Raphaël Reverdy <raphael.reverdy@akretion.com>

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association**
   :target: https://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit https://odoo-community.org.
