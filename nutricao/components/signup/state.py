# python3
# -*- coding: utf-8 -*-
# pylint: disable=(too-few-public-methods, too-many-arguments, too-many-locals, too-many-statements, line-too-long, inherit-non-class, broad-exception-caught,logging-fstring-interpolation,)
import json
import logging
import reflex as rx
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound, MultipleResultsFound
from entities import AuditLog, Login, UserContactDocument, Person, ContactDocument, ContDocID
from utils import get_trace_back_from_exception


VERIFY_EMAIL_MSG = "Por favor, verifique o seu e-mail. Os e-mails não são iguais."
VERIFY_PASSWORD_MSG = "Por favor, verifique a sua senha. As senhas não são iguais."
EXISTENT_EMAIL_MSG = "O e-mail informado já está cadastrado em nosso sistema"
EXISTENT_CPF_MSG = "O CPF informado já está cadastrado em nosso sistema"

logger = logging.getLogger()


class SignupFormState(rx.State):
    """State for the signup form."""

    cpf: str = ""

    password: str = ""
    confirm_password: str = ""

    email: str = ""
    confirm_email: str = ""

    async def _store_audit(self, db_session, json_data: str):
        """Store audit log in the database."""
        # Create a new AuditLog entry
        try:
            audit_log = AuditLog(action="signup", target_data=json_data)
            db_session.add(audit_log)
            logger.debug("Storing audit from db_session")
        except Exception as e:
            err_msg = "Erro ao gravar dados de auditoria"
            logger.error(err_msg)
            raise ValueError(err_msg, e) from e

    async def _exists_document(self, db_session, item: tuple) -> bool:
        """Check if the document already exists."""
        query = select(UserContactDocument).where(UserContactDocument.name == item[0])
        try:
            resultset = await db_session.exec(query)
            resultset.one()
            logger.warning(f"Document {item[0]} already exists on database")
            raise ValueError(item[1])
        except NoResultFound:
            logger.debug(f"Document {item[0]} does not exist on database")
            return False
        except MultipleResultsFound:
            logger.critical(f"Encontrado multiplos registros com documento {item[0]}")
            raise

    async def exists_document_on_database(self, db_session, form_data: dict) -> bool:
        """Verify if the fields are valid."""
        # Check if the fields are valid (e.g., not empty, valid format)
        # You can implement your own validation logic here
        verify_list: list = (
            (form_data["cpf"], EXISTENT_CPF_MSG),
            (form_data["login_id"], EXISTENT_EMAIL_MSG),
        )
        for item in verify_list:
            logger.debug(f"Verificando documento {item[0]} no banco de dados")
            await self._exists_document(db_session, item)

    def _verify_password(self, form_data: dict):
        """Verify if the password and confirm password match."""
        if form_data["password"] != form_data["confirmPassword"]:
            logger.debug(VERIFY_PASSWORD_MSG)
            raise ValueError(VERIFY_PASSWORD_MSG)

    @staticmethod
    def _verify_email(login_id, confirm_email) -> bool:
        """Verify if the email and confirm email match."""
        if login_id != confirm_email:
            logger.debug(VERIFY_EMAIL_MSG)
            raise ValueError(VERIFY_EMAIL_MSG)

    async def _add_new_user(self, db_session, form_data: dict):
        """Add a new user to the database."""
        # Create a new user and add it to the database
        # You can implement your own logic to create a new user here
        try:
            doctype_cpf = await db_session.get(ContactDocument, ContDocID.CPF)
            doctype_email = await db_session.get(ContactDocument, ContDocID.EMAIL)
            doc_cpf = UserContactDocument(contdoc=doctype_cpf, name=form_data["cpf"], is_main=True)
            doc_email = UserContactDocument(
                contdoc=doctype_email, name=form_data["login_id"], is_main=True
            )
            new_person = Person(name=form_data["name"])
            new_person.add(doc_cpf)
            new_person.add(doc_email)
            db_session.add(new_person)
            login = Login(user=new_person, password=form_data["password"])
            db_session.add_all((new_person, login))
        except Exception as e:
            err_msg = f"Erro ao efetuar o seu novo cadastro: {str(e)}"
            logger.error(err_msg)
            get_trace_back_from_exception(logger, e)
            raise ValueError(err_msg, e) from e

    @rx.event
    async def on_submit(self, form_data: dict):
        """Handle form submission."""
        # Handle form submission logic here
        # For example, you can access the form data using event.target.elements
        # and perform any necessary actions (e.g., sending data to a server)
        async with rx.asession() as db_session:
            try:
                self._verify_password(form_data)
                self._verify_email(form_data["login_id"], form_data["confirmEmail"])
                # Create a new AuditLog entry
                await self.exists_document_on_database(db_session, form_data)
                await self._add_new_user(db_session, form_data)
                await self._store_audit(db_session, json.dumps(form_data))
                await db_session.commit()
                logger.debug("Signup OK")
                yield rx.redirect("/signup_ok")
            except ValueError as err:
                await db_session.rollback()
                logger.error("Ocorreu um erro ao incluir essa nova inscrição")
                yield rx.toast.error(str(err))

    @rx.event
    async def verify_password(self):
        """Verify if the password and confirm password match."""
        if self.password != self.confirm_password:
            logger.debug(VERIFY_PASSWORD_MSG)
            yield rx.toast.error(VERIFY_PASSWORD_MSG)

    @rx.event
    async def verify_email(self):
        """Verify if the email and confirm email match."""
        if self.email != self.confirm_email:
            logger.debug(VERIFY_EMAIL_MSG)
            yield rx.toast.error(VERIFY_EMAIL_MSG)

    @rx.event
    async def on_load(self):
        """Handle form load."""
        self.cpf: str = ""
        self.password: str = ""
        self.confirm_password: str = ""

        self.email: str = ""
        self.confirm_email: str = ""

    @rx.event
    async def on_blur_cpf(self):
        """handle on blur event on cpf"""
        logger.debug(f"Verifying ID: {self.cpf}")
        try:
            async with rx.asession() as db_session:
                await self._exists_document(db_session, (self.cpf, EXISTENT_CPF_MSG))
        except ValueError as e:
            yield rx.toast.error(str(e))

    @rx.event
    async def on_blur_email(self):
        """handle on blur event on confirm email field"""
        logger.debug(f"Verifying e-mail: {self.email} and {self.confirm_email}")
        try:
            self._verify_email(self.email, self.confirm_email)
        except ValueError as e:
            yield rx.toast.error(str(e))
