from odoo import models

class MailMail(models.Model):
    _inherit = "mail.mail"

    def _send(self, auto_commit=False, raise_exception=False, smtp_session=None, alias_domain_id=False):
        ''' Extend _send to add our custom mailserver and email_from if they exist on active model. '''
        # Custom values for email_from and mail_server_id for active model
        model = self.env["ir.model"].sudo().search([("model", "=", self._context.get('active_model'))])
        custom_mailserver = model.outgoing_mailserver_id
        custom_email = model.outgoing_email

        for mail_id in self.ids:
            mail = self.browse(mail_id)

            if mail.state != 'outgoing':
                continue

            # Set the custom email_from and mail_server_id for the current mail
            if custom_email:
                mail.email_from = custom_email
            if custom_mailserver:
                mail.mail_server_id = custom_mailserver

            # Call the super method to proceed with sending
            super(MailMail, mail)._send(
                auto_commit=auto_commit,
                raise_exception=raise_exception,
                smtp_session=smtp_session,
                alias_domain_id=alias_domain_id,
            )
        return True
