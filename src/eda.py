import streamlit as st
import pandas as pd


class BCW_Explorer:
    '''
    Class to explore the dataset
    '''
    def __init__(self, nrows=100):
        '''
        '''
        # @st.cache
        def load_data() -> None:
            # defines header for the dataframe following the documentation
            # header =\
            #     ['id', 'label'] +\
            #     [
            #         '{0}_{1}'.format(attribute, summary)
            #         for summary in ['mean', 'std', 'mean_3max']
            #         for attribute in [
            #             'radius', 'texture',
            #             'circumference', 'area',
            #             'smoothness', 'density',
            #             'concavity_intensity', 'concavity_count',
            #             'symmetry', 'fractal_dimension'
            #         ]
            #     ]

            try:
                data = pd.read_csv(
                    'data/raw/wdbc.data',
                    header=None,
                    # names=pd.np.array(header),
                    nrows=nrows
                )

            except Exception as e:
                print('Error while loading data: {0}'.format(e))

            # drops unnecessary id column
            data = data.drop(0, axis=1)

            # transform labels into binary
            labels = data[1].map({'M': 1, 'B': 0}).astype('Int8')

            # enforcing multi-level index
            summaries = ['mean', 'std', 'mean_max3']
            multilevel =\
                pd.concat(
                    [
                        data[cols]
                        .rename(
                            columns={
                                x: attribute
                                for x, attribute
                                in zip(
                                    cols,
                                    [
                                        'radius', 'texture',
                                        'circumference', 'area',
                                        'smoothness', 'density',
                                        'concavity_intensity',
                                        'concavity_count',
                                        'symmetry', 'fractal_dimension'
                                    ]
                                )
                            }
                        )
                        for cols in pd.np.array_split(
                            range(2, 32), len(summaries)
                        )
                    ],
                    axis=1,
                    keys=summaries,
                    names=['summaries', 'attributes']
                )

            multilevel['label'] = labels
            return multilevel

        self.data = load_data()


# st.title('Elogroup - Data Scientist Applicant')
# st.header('Case: Breast Cancer Wisconsin EDA')
# eda = BCW_Explorer()
# st.bar_chart(eda.data.xs('mean', level='summaries', axis=0))
