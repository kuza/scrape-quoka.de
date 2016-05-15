from sqlalchemy import Column, String, Integer
from .connection import Base, engine


class Quoka(Base):
    __tablename__ = 'quoka'

    id = Column(Integer, primary_key=True)
    Boersen_ID = Column(Integer)
    OBID = Column(Integer)
    erzeugt_am = Column(Integer)
    Anbieter_ID = Column(String(20))
    Anbieter_ObjektID = Column(String(100))
    Immobilientyp = Column(String(50))
    Immobilientyp_detail = Column(String(200))
    Vermarktungstyp = Column(String(50))
    Land = Column(String(30))
    Bundesland = Column(String(50))
    Bezirk = Column(String(150))
    Stadt = Column(String(150))
    PLZ = Column(String(10))
    Strasse = Column(String(100))
    Hausnummer = Column(String(40))
    Uberschrift = Column(String(500))
    Beschreibung = Column(String(15000))
    Etage = Column(Integer)
    Kaufpreis = Column(Integer)
    Kaltmiete = Column(Integer)
    Warmmiete = Column(Integer)
    Nebenkosten = Column(Integer)
    Zimmeranzahl = Column(Integer)
    Wohnflaeche = Column(Integer)
    Monat = Column(Integer)
    url = Column(String(1000))
    Telefon = Column(String(100))
    Erstellungsdatum = Column(Integer)
    Gewerblich = Column(Integer)

Base.metadata.create_all(bind=engine)
