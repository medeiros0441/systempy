import React from 'react';

const Table = ({ dataHeader, columns, rows }) => {
  return (
    <div className="my-3 container p-1">
      {/* Título e botão de ação */}
      <div className="d-flex container justify-content-between mb-2 row container mx-auto p-1">
        <h1 className="text-start col" style={{ fontSize: '1.0rem' }}>
          <i className={`bi bi-${dataHeader.icon}-fill`}></i> {dataHeader.title}
        </h1>
        <button
          onClick={dataHeader.onClickBtn}
          type="button"
          className="btn btn-success btn-sm col-auto mx-auto me-sm-2"
          style={{ fontSize: '0.8rem' }}
        >
          <i className={`bi bi-${dataHeader.iconBtn} me-1`} style={{ fontSize: '0.8rem' }}></i>
          {dataHeader.buttonText}
        </button>
      </div>

      {/* Tabela */}
      <div className="container p-3 mx-auto bg-dark rounded">
        <div className="table-responsive">
          <table className="table table-hover table-sm table-dark">
            <thead>
              <tr className="font-monospace text-start" style={{ fontSize: '0.8rem' }}>
                {columns.map((colTitle, index) => (
                  <th key={index} scope="col" className="mx-auto text-center">
                    {colTitle}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="table-group-divider">
              {rows.map((row, rowIndex) => (
                <tr key={rowIndex} className="font-monospace text-start" style={{ fontSize: '0.8rem' }}>
                  {row.data.map((cell, cellIndex) => (
                    <td key={cellIndex} className="mx-auto text-center">
                      {cell}
                    </td>
                  ))}
                  <td className="text-end">
                    <div className="btn-group-sm btn-group" role="group" aria-label="Ações">
                      {row.actions.map((action, actionIndex) => (
                        <button
                          key={actionIndex}
                          type="button"
                          className={`btn btn-${action.type} btn-sm`}
                          onClick={action.onClick}
                          title={action.name}
                        >
                          <i className={action.icon}></i>
                        </button>
                      ))}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Table;
