from sqlalchemy import String, Column, Integer, Float, Boolean, select, Index

from .Base import Base
from .connect import engine, session


class Qualifications(Base):
    __tablename__ = "qualifications"
    
    __table_args__ = (
        Index(
            "ix_qualifications_am_aa",
            "am",
            "aa"
        ),
    )

    # Primary key
    # Every SQLAlchemy table should have a primary key named 'id'

    id = Column(Integer, primary_key=True)

    educator_id =  Column(Integer, index=True)

    # --------------------------------------------------
    # Metadata
    # --------------------------------------------------

    aa                 = Column(Integer, index=True)
    am                 = Column(Integer, index=True)
    specialization     = Column(String(length=255), index=True)
    year_of_import     = Column(String(length=255), index=True)
    pinakas_katataksis = Column(String(length=255), index=True) #2EA 2GE
    file               = Column(String(length=255))
    total_score        = Column(Float)

    # --------------------------------------------------
    # Academic qualifications
    # --------------------------------------------------

    vasikos_titlos_spoudon = Column(Float)
    deutero_ptyxio_aei = Column(Float)
    didaktoriko_diploma = Column(Float)

    arithmos_autotelon_metaptyxiakon_titlon_i_integrated_masters = Column(Integer)
    monades_metaptyxiakon_titlon_synolika = Column(Float)

    ptyxio_paidagogikou_eae_monon_gia_pe61_pe71 = Column(Boolean)
    ptyxio_tefaa_me_kyria_eidikotita_eae_monon_gia_pe11 = Column(Boolean)

    epimorfosi_aei_toulaxiston_300_oron_7_minon = Column(Float)

    synolo_monadon_akadimaikon_prosonton = Column(Float)

    # --------------------------------------------------
    # Foreign languages
    # --------------------------------------------------

    aristi_gnosi_xenon_glosson = Column(Integer)
    poly_kali_gnosi_xenon_glosson = Column(Integer)
    kali_gnosi_xenon_glosson = Column(Integer)

    synolo_monadon_xenon_glosson_eos_2 = Column(Float)

    # --------------------------------------------------
    # Computer skills
    # --------------------------------------------------

    gnosi_xeirismou_iy = Column(Float)

    # --------------------------------------------------
    # Teaching experience
    # --------------------------------------------------

    mines_ekpaideutikis_proypiresias = Column(Float)
    monades_ekpaideutikis_proypiresias = Column(Float)

    mines_ekpaideutikis_proypiresias_se_dysprosita = Column(Float)
    monades_ekpaideutikis_proypiresias_se_dysprosita = Column(Float)

    # 3-month contracts 2020-2021
    mines_ekp_proyp_3minis_diarkeias_2020_2021 = Column(Float)
    monades_ekp_proyp_3minis_diarkeias_2020_2021 = Column(Float)

    # 3-month contracts 2021-2022
    mines_ekp_proyp_3minis_diarkeias_2021_2022 = Column(Float)
    monades_ekp_proyp_3minis_diarkeias_2021_2022 = Column(Float)

    # 3-month contracts / hard-to-reach areas 2020-2021
    mines_ekp_proyp_3minis_diarkeias_dysprosita_2020_2021 = Column(Float)
    monades_ekp_proyp_3minis_diarkeias_dysprosita_2020_2021 = Column(Float)

    # 3-month contracts / hard-to-reach areas 2021-2022
    mines_ekp_proyp_3minis_diarkeias_dysprosita_2021_2022 = Column(Float)
    monades_ekp_proyp_3minis_diarkeias_dysprosita_2021_2022 = Column(Float)

    # Private education
    mines_ekp_proyp_stin_idiotiki_ekpaideusi = Column(Float)
    monades_ekp_proyp_stin_idiotiki_ekpaideusi = Column(Float)

    # Digital tutoring
    mines_ekp_proyp_sto_psifiako_frontistirio = Column(Float)
    monades_ekp_proyp_sto_psifiako_frontistirio = Column(Float)

    synolo_monadon_ekpaideutikis_proypiresias = Column(Float)

    # --------------------------------------------------
    # Children
    # --------------------------------------------------

    arithmos_teknon = Column(Integer)
    monades_teknon = Column(Float)

    # --------------------------------------------------
    # Disability
    # --------------------------------------------------

    pososto_anapirias = Column(Float)
    monades_anapirias = Column(Float)

    # --------------------------------------------------
    # Special qualifications
    # --------------------------------------------------

    protaksi_logo_paidagogikis_didaktikis_eparkeias = Column(Boolean)

    braille = Column(Boolean, default=False, nullable=False)
    elliniki_noimatiki_glossa = Column(Boolean, default=False, nullable=False)

    # --------------------------------------------------
    # Ranking / lottery
    # --------------------------------------------------

    seira_ilektronikis_klirosis_par_4_arthr_15_n_4765_2021 = Column(Integer)

    # --------------------------------------------------
    # Factory
    # --------------------------------------------------

    @staticmethod
    def createRow(row):
        qualifications = Qualifications()
        qualifications.updateRow(row)

        return qualifications

    # --------------------------------------------------
    # Update
    # --------------------------------------------------

    def updateRow(self, row):
        fields = [
            "aa",
            "am",
            "file",
            "specialization",
            "educator_id",
            "pinakas_katataksis",
            "year_of_import",
            "vasikos_titlos_spoudon",
            "deutero_ptyxio_aei",
            "didaktoriko_diploma",
            "arithmos_autotelon_metaptyxiakon_titlon_i_integrated_masters",
            "monades_metaptyxiakon_titlon_synolika",
            "ptyxio_paidagogikou_eae_monon_gia_pe61_pe71",
            "ptyxio_tefaa_me_kyria_eidikotita_eae_monon_gia_pe11",
            "epimorfosi_aei_toulaxiston_300_oron_7_minon",
            "synolo_monadon_akadimaikon_prosonton",
            "aristi_gnosi_xenon_glosson",
            "poly_kali_gnosi_xenon_glosson",
            "kali_gnosi_xenon_glosson",
            "synolo_monadon_xenon_glosson_eos_2",
            "gnosi_xeirismou_iy",
            "mines_ekpaideutikis_proypiresias",
            "monades_ekpaideutikis_proypiresias",
            "mines_ekpaideutikis_proypiresias_se_dysprosita",
            "monades_ekpaideutikis_proypiresias_se_dysprosita",
            "mines_ekp_proyp_3minis_diarkeias_2020_2021",
            "monades_ekp_proyp_3minis_diarkeias_2020_2021",
            "mines_ekp_proyp_3minis_diarkeias_2021_2022",
            "monades_ekp_proyp_3minis_diarkeias_2021_2022",
            "mines_ekp_proyp_3minis_diarkeias_dysprosita_2020_2021",
            "monades_ekp_proyp_3minis_diarkeias_dysprosita_2020_2021",
            "mines_ekp_proyp_3minis_diarkeias_dysprosita_2021_2022",
            "monades_ekp_proyp_3minis_diarkeias_dysprosita_2021_2022",
            "mines_ekp_proyp_stin_idiotiki_ekpaideusi",
            "monades_ekp_proyp_stin_idiotiki_ekpaideusi",
            "mines_ekp_proyp_sto_psifiako_frontistirio",
            "monades_ekp_proyp_sto_psifiako_frontistirio",
            "synolo_monadon_ekpaideutikis_proypiresias",
            "arithmos_teknon",
            "monades_teknon",
            "pososto_anapirias",
            "monades_anapirias",
            "protaksi_logo_paidagogikis_didaktikis_eparkeias",
            "braille",
            "elliniki_noimatiki_glossa",
            "seira_ilektronikis_klirosis_par_4_arthr_15_n_4765_2021",
            "total_score"
        ]

        for field in fields:
            if field in row:
                setattr(self, field, row[field])

    # --------------------------------------------------
    # Queries
    # --------------------------------------------------

    @staticmethod
    def findByEducatorID(educator_id):
        query = select(Qualifications).where(
            Qualifications.educator_id == educator_id
        )

        return session.scalars(query).all()


    def findBy(specialization, educator_id, am):
        query = select(Qualifications).where(
            Qualifications.educator_id == educator_id
        )
        query = query.where(
            Qualifications.specialization == specialization
        )
        query = query.where(
            Qualifications.am == am
        )

        return session.scalars(query).all()

Base.metadata.create_all(engine)